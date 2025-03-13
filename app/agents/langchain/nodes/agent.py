from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants
from app.utils.prompts import prompts

def agent(state: AgentState):
    """
    Agent that decides whether to use tools or not
    """
    tools = state['tools']
    
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    messages = state["messages"]

    agent = create_react_agent(
        model,
        tools,
        prompt=prompts.BLOG_SEARCH_PROMPT,
    )

    agent_response = agent.invoke({"messages": messages})
    
    return agent_response