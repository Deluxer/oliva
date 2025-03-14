from langgraph.graph import END, START, StateGraph
from app.agents.core.agent_state import AgentState
from functools import lru_cache
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.core.base_agent import BaseAgent
from app.agents.langchain.factory import AgentFactory
from app.utils.types import ToolType, EdgeType, NodeType
from app.utils.prompts import prompts

class SearchAmazonProductsAgentByJson(BaseAgent):
    """Agent specialized in searching amazon products"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__(
                tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON],
                edge_types=[EdgeType.GRADE_DOCUMENTS],
                node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
            )
            self._workflow = None
            self._initialized = True

    @lru_cache(maxsize=1)
    def prepare(self):
        """Initialize workflow components and configure the graph structure."""
        self._workflow = StateGraph(AgentState)

        events = self.setup_events()
        tools, edges, nodes = events
        agent = self.inject_tools_and_template(tools, nodes[NodeType.AGENT], prompts.AGENT_PROMPT_BY_JSON)

        self._workflow.add_node("agent", agent)
        self._workflow.add_node("retrieve", ToolNode(tools))
        self._workflow.add_node("rewrite", nodes[NodeType.REWRITE])
        self._workflow.add_node("generate", nodes[NodeType.GENERATE])
        self._workflow.add_edge(START, "agent")
        self._workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "retrieve", END: END}
        )
        self._workflow.add_conditional_edges(
            "retrieve",
            edges[EdgeType.GRADE_DOCUMENTS],
            {"generate": "generate", "rewrite": "rewrite"}
        )
        self._workflow.add_edge("generate", END)

    def process(self, input_state: dict):
        self.prepare()
        
        result = AgentFactory.create_agent(self._workflow, input_state)
        return result

    def studio(self):
        """Compile workflow for LangGraph Studio"""
        self.prepare()
        return self._workflow.compile()

agent = SearchAmazonProductsAgentByJson()

# Initialize graph for LangGraph Studio
graph = agent.studio()