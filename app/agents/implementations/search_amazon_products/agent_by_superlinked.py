from langgraph.prebuilt import tools_condition
from langgraph.graph import END, START

from app.agents.core.base_agent import BaseAgent
from app.utils.types import ToolType, EdgeType, NodeType

class SearchAmazonProductsAgentBySuperlinked(BaseAgent):
    """Agent specialized in searching amazon products"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED],
            edge_types=[EdgeType.GRADE_DOCUMENTS],
            node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
        )

    def prepare(self):
        if self._workflow:
            return self._workflow

        events = self.setup_events()
        tools_retriever, edges, nodes = events

        self.workflow.add_node("agent", nodes[NodeType.AGENT])
        self.workflow.add_node("retrieve", self.to_func(tools_retriever))
        self.workflow.add_node("generate", nodes[NodeType.GENERATE])
        self.workflow.add_node("rewrite", nodes[NodeType.REWRITE])
        self.workflow.add_conditional_edges(
            "retrieve",
            edges[EdgeType.GRADE_DOCUMENTS],
            {"generate": "generate", "rewrite": "rewrite"}
        )
        return self.workflow
        
    def graph(self):
        self.workflow.add_edge(START, "agent")
        self.workflow.add_edge("generate", END)
        self.workflow.add_edge("rewrite", "agent")
        self._workflow = self.workflow.compile()        
        return self._workflow

    def process(self, input_data: dict):
        if not self._workflow:
            self.prepare()
            self.graph()
        
        query = input_data.get("query", "")
        result = self.implement({ "query": query })
        return result