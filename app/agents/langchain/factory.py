from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from app.utils.helpers import stream

class AgentFactory:
    @staticmethod
    def create_agent(workflow: StateGraph, input_data: dict):
        """Execute the agent workflow without recompiling it"""

        current_query = input_data.get("query", "")

        if not isinstance(current_query, str) or not current_query.strip():
            return {"messages": ["No valid query provided."]}

        graph = workflow.compile()

        formatted_input = {
            "messages": HumanMessage(content=str(current_query)),
            "tools": input_data.get("tools", []),
            "rewrite_count": 0,
        }

        return stream(graph, formatted_input)