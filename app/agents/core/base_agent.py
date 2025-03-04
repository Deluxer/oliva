from typing import Any, Dict, List, Optional, Sequence

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
        self.tool_provider = ToolProvider()
        self.edge_provider = EdgeProvider()
        self.nodes_provider = NodesProvider()
        self.workflow = StateGraph(AgentState)
        
    def setup_tools(self) -> List[Any]:
        """Get tools based on specified types or all available tools if none specified"""
        return self.tool_provider.get_tools_by_types(self.tool_types)

    def setup_edges(self) -> List[Any]:
        """Get edges based on specified types or all available edges if none specified"""
        return self.edge_provider.get_edges_by_types(self.edge_types)
    
    def setup_nodes(self) -> List[Any]:
        """Get nodes based on specified types or all available nodes if none specified"""
        return self.nodes_provider.get_nodes_by_types(self.node_types)
    
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
        self.current_query = input_data.get("query", "")
        response = self.run(workflow)
        
        # Format input for the workflow
        formatted_input = {
            "messages": [
                HumanMessage(content=self.current_query),
            ]
        }
        
        # Execute workflow and collect results
        results = []
        for output in response.stream(formatted_input):
            for key, value in output.items():
                results.append({
                    "node": key,
                    "output": value
                })
        
        return {"results": results}
    
    @property
    def agent_type(self) -> str:
        return "blog_search"