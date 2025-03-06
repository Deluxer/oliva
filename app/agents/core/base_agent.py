from typing import Any, Dict, List, Optional, Sequence

from app.utils.helpers import invoke, stream
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage

from app.agents.langchain.interface.events import AgentEvents
from app.agents.langchain.factory import AgentFactory
from app.agents.langchain.state import AgentState
from app.agents.langchain.tools.tools import ToolProvider
from app.agents.langchain.edges.edges import EdgeProvider
from app.agents.langchain.nodes.nodes import NodesProvider
from app.utils.types import EdgeType, ToolType, NodeType

class BaseAgent():
    """Base class for all agents"""

    def __init__(self, tool_types: Optional[Sequence[ToolType]] = None, edge_types: Optional[Sequence[EdgeType]] = None, node_types: Optional[Sequence[NodeType]] = None):
        self.tool_types = tool_types
        self.edge_types = edge_types
        self.node_types = node_types
        self.workflow = StateGraph(AgentState)
        self._tool_provider = None
        self._edge_provider = None
        self._nodes_provider = None

    @property
    def tool_provider(self):
        if self._tool_provider is None:
            self._tool_provider = ToolProvider()
        return self._tool_provider

    @property
    def edge_provider(self):
        if self._edge_provider is None:
            self._edge_provider = EdgeProvider()
        return self._edge_provider

    @property
    def nodes_provider(self):
        if self._nodes_provider is None:
            self._nodes_provider = NodesProvider()
        return self._nodes_provider

    def setup_tools(self) -> List[Any]:
        """Get tools based on specified types or all available tools if none specified"""
        return self.tool_provider.get_items_by_types(self.tool_types)

    def setup_edges(self) -> List[Any]:
        """Get edges based on specified types or all available edges if none specified"""
        return self.edge_provider.get_items_by_types(self.edge_types)
    
    def setup_nodes(self) -> List[Any]:
        """Get nodes based on specified types or all available nodes if none specified"""
        return self.nodes_provider.get_items_by_types(self.node_types)
    
    def setup_events(self) -> Any:
        """Initialize the RAG workflow for blog posts using AgentFactory
        
        Returns:
            A compiled workflow with agent, retrieval, rewrite and generate nodes
        """
        # Initialize tools - handle both instances and provider classes
        tools = self.setup_tools()
        edges = self.setup_edges()
        nodes = self.setup_nodes()

        return AgentEvents.mapper(tools, edges, nodes)

    def run(self, workflow: StateGraph) -> Any:
        return AgentFactory.create_agent(workflow)
    
    def execute(self, workflow: StateGraph, input_data: Dict[str, Any]) -> Dict[str, Any]:
        current_query = input_data.get("query", "")
        graph = self.run(workflow)
        
        formatted_input = {
            "messages": [
                HumanMessage(content=current_query),
            ]
        }
        
        return stream(graph, formatted_input)
    
    @property
    def agent_type(self) -> str:
        return "blog_search"