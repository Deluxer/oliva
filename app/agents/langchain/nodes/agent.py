from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants

def agent(state: AgentState):
    """
    Agent that decides whether to use tools or not
    """
    tools_list = state['tools']
    tools = list(tools_list.values())
    
    model = ChatOpenAI(temperature=0, streaming=True, model=constants.LLM_MODEL)
    messages = state["messages"]
    prompt = """
        You are an assistant that helps users find products.
        If the user asks about products, always use the 'search_amazon_products_by_superlinked' tool.
    """
    agent = create_react_agent(
        model,
        tools,
        prompt=prompt,
        debug=False
    )

    agent_response = agent.invoke({"messages": messages})
    print(agent_response)
    
    return agent_response