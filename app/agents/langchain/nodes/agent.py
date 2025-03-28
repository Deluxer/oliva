from langgraph.types import Command
from typing import Literal
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agents.core.agent_state import SubGraphAgentState
from app.utils.constants import constants

def agent(state: SubGraphAgentState) -> Command[Literal['supervisor']]:
    """
    Agent that decides whether to use tools or not
    """
    tools = state["tools"]
    template = state['template']
    memory = MemorySaver()
    model = ChatOpenAI(temperature=0, model=constants.LLM_MODEL)
    messagesState = state["messages"]
    agent = create_react_agent(
        model,
        tools,
        prompt=template,
        checkpointer=memory
    )

    agent_response = agent.invoke({"messages": messagesState})
    messages = agent_response["messages"]

    response = Command(
        goto = 'supervisor',
        update={"next": 'FINISH', "messages": messages},
        graph=Command.PARENT
    )

    return response
