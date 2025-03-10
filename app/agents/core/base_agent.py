from typing import Any, List, Optional, Sequence, Type, Union

from langgraph.graph import StateGraph

from app.agents.langchain.interface.base_provider import BaseProvider

from app.agents.langchain.interface.events import AgentEvents
from app.agents.core.agent_state import AgentState
from app.agents.langchain.tools.tools import ToolProvider
from app.agents.langchain.edges.edges import EdgeProvider
from app.agents.langchain.nodes.nodes import NodeProvider
from app.utils.types import EdgeType, ToolType, NodeType

class BaseAgent():
    """Base class for all agents"""
    def __init__(
        self,
        tool_types: Optional[Sequence[ToolType]] = None, 
        edge_types: Optional[Sequence[EdgeType]] = None, 
        node_types: Optional[Sequence[NodeType]] = None
    ):
        self.tool_types = tool_types
        self.edge_types = edge_types
        self.node_types = node_types
        self._tool_provider = None
        self._edge_provider = None
        self._nodes_provider = None
        self.workflow = None

    # def config(
    #     self,
    #     tool_types: Optional[Sequence[ToolType]] = None, 
    #     edge_types: Optional[Sequence[EdgeType]] = None, 
    #     node_types: Optional[Sequence[NodeType]] = None
    # ):
    #     self.tool_types = tuple(tool_types) if tool_types else None
    #     self.edge_types = tuple(edge_types) if edge_types else None
    #     self.node_types = tuple(node_types) if node_types else None

    @property
    def tool_provider(self) -> ToolProvider:
        if self._tool_provider is None:
            self._tool_provider = ToolProvider()
        return self._tool_provider

    @property
    def edge_provider(self) -> EdgeProvider:
        if self._edge_provider is None:
            self._edge_provider = EdgeProvider()
        return self._edge_provider

    @property
    def nodes_provider(self) -> NodeProvider:
        if self._nodes_provider is None:
            self._nodes_provider = NodeProvider()
        return self._nodes_provider

    # @lru_cache(maxsize=1)
    def setup_tools(self) -> List[Any]:
        """Get tools based on specified types or all available tools if none specified"""
        return self.tool_provider.get_items_by_types(self.tool_types)

    # @lru_cache(maxsize=1)
    def setup_edges(self) -> List[Any]:
        """Get edges based on specified types or all available edges if none specified"""
        return self.edge_provider.get_items_by_types(self.edge_types)
    
    # @lru_cache(maxsize=1)
    def setup_nodes(self) -> List[Any]:
        """Get nodes based on specified types or all available nodes if none specified"""
        return self.nodes_provider.get_items_by_types(self.node_types)
    
    def setup_events(self) -> Any:
        """Initialize workflow components when needed"""
        self.workflow = StateGraph(AgentState)
        tools = self.setup_tools()
        edges = self.setup_edges()
        nodes = self.setup_nodes()

        return AgentEvents.mapper(tools, edges, nodes)

    def to_func(self, event_list: Union[List[Any], Type[BaseProvider]]) -> List[Any]:
        return AgentEvents.transform(event_list)