from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import END, START

from app.agents.core.base_agent import BaseAgent
from app.agents.langchain.factory import AgentFactory
from app.utils.types import ToolType, EdgeType, NodeType

class SearchAmazonProductsAgentByJson(BaseAgent):
    """Agent specialized in searching amazon products"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON],
            edge_types=[EdgeType.GRADE_DOCUMENTS],
            node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
        )

    def prepare(self, input_state: dict):
        events = self.setup_events()
        tools, edges, nodes = events
        tools_list = list(tools.values())
        input_state["tools"] = tools_list
        
        self.workflow.add_node("agent", nodes[NodeType.AGENT])
        self.workflow.add_node("retrieve", ToolNode(tools_list))
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

    def process(self, input_state: dict):
        self.prepare(input_state)
        
        result = AgentFactory.create_agent(self.workflow, input_state)
        return result