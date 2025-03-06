from langgraph.prebuilt import tools_condition
from langgraph.graph import END, START

from app.agents.core.base_agent import BaseAgent
from app.utils.types import ToolType, EdgeType, NodeType

class SearchAmazonProductsAgentByJson(BaseAgent):
    """Agent specialized in searching amazon products"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON],
            edge_types=[EdgeType.GRADE_DOCUMENTS],
            node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
        )

    def prepare(self):
        events = self.setup_events()
        retrieve, edges, nodes = events

        self.workflow.add_node("agent", nodes[NodeType.AGENT])
        self.workflow.add_node("retrieve", retrieve)
        self.workflow.add_node("rewrite", nodes[NodeType.REWRITE])
        self.workflow.add_node("generate", nodes[NodeType.GENERATE])
        
        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "retrieve", END: END}
        )
        
        self.workflow.add_conditional_edges(
            "retrieve",
            edges[EdgeType.GRADE_DOCUMENTS],
            {"generate": "generate", "rewrite": "rewrite"}
        )
        
        self.workflow.add_edge("generate", END)
        self.workflow.add_edge("rewrite", "agent")

        return self.workflow

    def process(self):
        result = self.execute(self.prepare(), {
            "query": "Find books under $20",
            "filters": {
                "category": 'Books'
            }
        })
        return result