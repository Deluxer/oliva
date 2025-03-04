from typing import Any, Dict, Literal

from app.agents.langchain.nodes.rewriter import rewrite
from app.agents.langchain.nodes.agent import agent
from app.agents.langchain.nodes.generate import generate
from app.utils.types import NodeType
from app.agents.langchain.base.nodes import BaseNodesProvider

class NodesProvider(BaseNodesProvider):
    """Node provider for blog post related operations"""
    
    def __init__(self):
        self._initialize_nodes()
    
    def _initialize_nodes(self):
        """Initialize available nodes"""
        self._nodes = {
            NodeType.AGENT: agent,
            NodeType.GENERATE: generate,
            NodeType.REWRITE: rewrite,
        }
    
    def get_nodes(self) -> Dict[NodeType, Any]:
        """Get all available nodes"""
        return self._nodes
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate edge condition"""
        # Get the first available edge handler
        if self._nodes:
            node_handler = next(iter(self._nodes.values()))
            return node_handler(state)
        return "generate"  # Default fallback