from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.types import Command
from langchain.schema import BaseStore
from typing import TypedDict, Literal
import uuid
from datetime import datetime

from app.utils.prompts import prompts
from app.utils.constants import constants
from app.agents.core.agent_state import AgentState

supervisor_llm = ChatOpenAI(model=constants.LLM_MODEL)

class SupervisorOutput(TypedDict):
    next: Literal["blog_post_agent", "amazon_products_agent", "FINISH"]
    task_description_for_agent: str
    message_completion_summary: str

def supervisor(
    state: AgentState,
    config: RunnableConfig,
    *,
    store: BaseStore
) -> Command[Literal["blog_post_agent", "amazon_products_agent", END]]:
    """
    This node is responsible for delegating tasks to other agents.
    It first checks the semantic memory for similar previous queries and their results.
    If a similar query exists, it may reuse the results or decide to refresh them.
    Otherwise, it delegates the task to the appropriate agent.
    """
    user_id = config["configurable"]["user_id"]
    chat_id = config["configurable"]["chat_id"]

    # Get the initial query
    initial_query = state["messages"][0].content

    if state.get("next") == "FINISH":
        response = state["messages"][-1].content
        memory_text = f"User Query: {initial_query}\nAgent Response: {response}"
        
        store.put(
            namespace=f"{user_id}:{chat_id}:memories",  
            key=str(uuid.uuid4()),
            value={
                "query": initial_query,
                "response": response,
                "memory": memory_text,  
                "created_at": datetime.now().isoformat(),
                "type": "conversation"
            },
            index=["memory"]  
        )        
        return Command(goto=END, update={"next": END})

    # Get the current user query
    current_query = state["messages"][-1].content

    memories = store.search(
        namespace=f"{user_id}:{chat_id}:memories",  
        query=current_query,
        limit=3
    )

    if(memories):
        evaluation_result = store.evaluate(query=current_query, memories=memories)
        if isinstance(evaluation_result, str):
            return Command(goto=END, update={"next": END, "messages": evaluation_result})
        elif evaluation_result:
            memory_response = memories[0]["value"]["response"]
            return Command(goto=END, update={"next": END, "messages": memory_response})

    members = ["blog_post_agent", "amazon_products_agent"]
    agent_members_prompt_final = f"""
    blog_post_agent:
        - Prompt: {prompts.BLOG_SEARCH_PROMPT}
    amazon_products_agent:
        - Prompt: {prompts.AMAZON_SEARCH_PROMPT}
    """
    supervisor_system_prompt = prompts.supervisor_system_prompt(members, agent_members_prompt_final)
    messages = [{"role": "system", "content": supervisor_system_prompt}] + state["messages"]
    response = supervisor_llm.with_structured_output(SupervisorOutput).invoke(messages)
    goto = response["next"]

    if goto == "FINISH":
        return Command(goto=END, update={"next": END, "messages": response["message_completion_summary"]})

    new_messages = [{"role": "assistant", "content": response["task_description_for_agent"]}]
    return Command(goto=goto, update={"next": goto, "messages": new_messages})