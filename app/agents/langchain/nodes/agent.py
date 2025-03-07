from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from app.utils.constants import constants
from app.agents.langchain.tools.tools import ToolProvider
from app.utils.types import ToolType
from app.utils.prompts import prompts

def agent(state):
    """
    Agent that decides whether to use tools or not
    """
    print("---CALL AGENT---")

    tool_provider = ToolProvider()
    # Get the actual tool values, not the dictionary
    tool_instances = tool_provider.get_items_by_types([ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON])
    tools = [func() for func in tool_instances.values()]
    
    # Add system message to guide the agent
    messages = [
        SystemMessage(content=prompts.AMAZON_SEARCH_PROMPT)
    ] + state["messages"]
    
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}