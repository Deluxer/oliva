from langgraph.graph import END, START, StateGraph
from app.agents.core.agent_state import AgentState
from functools import lru_cache
from typing import Dict, Any

from app.agents.core.base_agent import BaseAgent
from app.agents.langchain.factory import AgentFactory
from app.utils.types import NodeType, ToolType

class SearchAmazonProductsAgentBySuperlinked(BaseAgent):
    """Agent specialized in searching amazon products"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__(
                tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED],
                edge_types=[],
                node_types=[NodeType.AGENT]
            )
            self._workflow = None
            self._initialized = True

    @lru_cache(maxsize=1)
    def prepare(self):
        """Initialize workflow components and configure the graph structure."""
        self._workflow = StateGraph(AgentState)
            
        events = self.setup_events()
        tools, _, nodes = events
        # Dynamic injection of tools into the agent node
        agent = self.inject_tools_in_node(tools, nodes[NodeType.AGENT])

        self._workflow.add_node("agent", agent)
        self._workflow.add_edge(START, "agent")
        self._workflow.add_edge("agent", END)

    def process(self, input_state: Dict[str, Any]) -> Dict[str, Any]:
        self.prepare()
        return AgentFactory.create_agent(self._workflow, input_state)

    def studio(self) -> Dict[str, Any]:
        """Compile workflow for LangGraph Studio"""
        self.prepare()
        return self._workflow.compile()

agent = SearchAmazonProductsAgentBySuperlinked()

# Initialize graph for LangGraph Studio
graph = agent.studio()