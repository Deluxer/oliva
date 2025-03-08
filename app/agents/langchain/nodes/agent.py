from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

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
    tool_instances = tool_provider.get_items_by_types([ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED])
    tools = [func() for func in tool_instances.values()]
    
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    messages = state["messages"]
    question = messages[0].content if messages else ""

    agent = create_react_agent(
        model,
        tools=tools,
    )

    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    
    return {"messages": messages + response["messages"]}