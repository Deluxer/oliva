from typing import Any, List, Optional, Sequence

from app.agents.langchain.interface.events import AgentEvents
from app.agents.core.agent_state import AgentState
from app.agents.langchain.tools.tools import ToolProvider
from app.agents.langchain.edges.edges import EdgeProvider
from app.agents.langchain.nodes.nodes import NodeProvider
from app.utils.types import EdgeType, ToolType, NodeType
from langgraph.types import Command

class BaseAgent():
    _instance = None
    """Base class for all agents"""
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
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
        tools = self.setup_tools()
        edges = self.setup_edges()
        nodes = self.setup_nodes()

        return AgentEvents.mapper(tools, edges, nodes)

    def inject_tools_and_template(self, tools, target_node, template):
        """Create a wrapper node that injects tools into the state before execution.
        
        Args:
            tools: Dictionary of tools to inject
            target_node: The original node function to wrap
            
        Returns:
            A wrapped node function that ensures tools are available in state
        """
        def wrapped_node(state: AgentState):
            command = Command(
                goto=None,
                update={
                    "tools": tools,
                    "template": template
                }
            )
            
            return target_node(state | command.update)
            
        return wrapped_node