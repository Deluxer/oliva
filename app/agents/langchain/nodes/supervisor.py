from langchain_openai import ChatOpenAI
from langgraph.graph import END
from langgraph.types import Command
from typing import TypedDict, Literal
from app.utils.constants import constants
from app.utils.prompts import prompts
from app.agents.core.agent_state import AgentState

# Create LLM instance
supervisor_llm = ChatOpenAI(model=constants.LLM_MODEL)

# Define the supervisor output schema
class SupervisorOutput(TypedDict):
    next: Literal["blog_post_agent", "amazon_products_agent", "FINISH"]
    task_description_for_agent: str
    message_completion_summary: str

def supervisor(state: AgentState) -> Command[Literal["blog_post_agent", "amazon_products_agent", END]]:
    """
    This node is responsible for delegating tasks to other agents.
    It takes the conversation history and the supervisor system prompt and
    combines them into a single input for the large language model.
    The large language model then generates a response that contains the
    next agent to go to and the task description for that agent.
    If the task is finished, it returns a command to go to the END node.
    Otherwise, it appends the tailored instructions to the conversation history
    and returns a command to go to the next agent.
    """

    members = ["blog_post_agent", "amazon_products_agent"]
    agent_members_prompt_final = """
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
        return Command(goto=END, update={"next": END})

    new_messages = [{"role": "user", "content": response["task_description_for_agent"]}]
    return Command(goto=goto, update={"next": goto, "messages": new_messages})