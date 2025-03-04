from langchain_openai import ChatOpenAI

from app.utils.constants import constants
from app.agents.langchain.tools.tools import ToolProvider
from app.utils.types import ToolType

def agent(state):
    """
    Agent that decides whether to use tools or not
    """
    print("---CALL AGENT---")
    tool_provider = ToolProvider()
    # Get the actual tool values, not the dictionary
    tools = list(tool_provider.get_tools_by_types([ToolType.AMAZON_PRODUCTS_SEARCH]).values())
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}