from langgraph.graph import END, START

from app.agents.core.base_agent import BaseAgent
from app.agents.langchain.factory import AgentFactory
from app.utils.types import NodeType, ToolType

class SearchAmazonProductsAgentBySuperlinked(BaseAgent):
    """Agent specialized in searching amazon products"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED],
            edge_types=[],
            node_types=[NodeType.AGENT]
        )

    def prepare(self, input_state: dict):
        events = self.setup_events()
        tools, _, nodes = events

        input_state["tools"] = tools
        self.workflow.add_node("agent", nodes[NodeType.AGENT])
        self.workflow.add_edge(START, "agent")
        self.workflow.add_edge("agent", END)

    def process(self, input_state: dict):
        self.prepare(input_state)
        
        result = AgentFactory.create_agent(self.workflow, input_state)
        print("######### result #########", result)
        return result