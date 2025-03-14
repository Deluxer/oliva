from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants

def agent(state: AgentState):
    """
    Agent that decides whether to use tools or not
    """
    tools = state["tools"]
    template = state['template']
    memory = MemorySaver()
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    messages = state["messages"]
    agent = create_react_agent(
        model,
        tools,
        prompt=template,
        checkpointer=memory
    )

    agent_response = agent.invoke(state)
    messages = agent_response["messages"]
    return Command(goto='supervisor', update={"next": 'supervisor', "messages": messages})