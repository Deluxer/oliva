from langgraph.graph import END, START, StateGraph
from app.agents.core.agent_state import AgentState
from functools import lru_cache
from typing import Dict, Any
from rich import print as rprint

from app.agents.core.base_agent import BaseAgent
from app.agents.implementations.blog_post.agent import graph as graph_blog
from app.agents.implementations.search_amazon_products.agent_by_superlinked import graph as graph_search_by_superlinked
from app.agents.langchain.factory import AgentFactory
from app.utils.types import NodeType

class SupervisorAgent(BaseAgent):
    """Agent specialized in supervising other agents"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__(
                tool_types=[],
                edge_types=[],
                node_types=[NodeType.SUPERVISOR]
            )
            self._workflow = None
            self._initialized = True        

    @lru_cache(maxsize=1)
    def prepare(self):
        """Initialize workflow components and configure the graph structure."""
        self._workflow = StateGraph(AgentState)
        events = self.setup_events()
        _, _, nodes = events
        
        self._workflow.add_node("supervisor", nodes[NodeType.SUPERVISOR])
        self._workflow.add_node("amazon_products_agent", graph_search_by_superlinked)
        self._workflow.add_node("blog_post_agent", graph_blog)
        
        self._workflow.add_edge(START, "supervisor")
        
        self._workflow.add_edge("blog_post_agent", END)
        self._workflow.add_edge("amazon_products_agent", END)
        
    def process(self, input_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through the workflow"""
        self.prepare()
        return AgentFactory.create_agent(self._workflow, input_state)

    def studio(self) -> Dict[str, Any]:
        """Compile workflow for LangGraph Studio"""
        self.prepare()
        return self._workflow.compile()

agent = SupervisorAgent()

graph = agent.studio()