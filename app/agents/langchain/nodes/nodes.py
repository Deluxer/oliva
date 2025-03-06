from typing import Any, Dict, Literal, Optional, Sequence
from app.agents.langchain.nodes.rewriter import rewrite
from app.agents.langchain.nodes.agent import agent
from app.agents.langchain.nodes.generate import generate
from app.utils.types import NodeType
from app.agents.langchain.interface.base_provider import BaseProvider

class NodesProvider(BaseProvider):
    """Node provider for blog post related operations"""
    
    def __init__(self):
        self._nodes = None
        self._node_mapping = {
            NodeType.AGENT: agent,
            NodeType.GENERATE: generate,
            NodeType.REWRITE: rewrite,
        }
        super().__init__()
    
    def _initialize_items(self):
        """Initialize nodes container"""
        if self._nodes is None:
            self._nodes = {}
    
    def get_items(self) -> Dict[NodeType, Any]:
        """Get all nodes"""
        self._initialize_items()
        return self._nodes
    
    def get_items_by_types(self, types: Optional[Sequence[NodeType]]) -> Dict[NodeType, Any]:
        """Return only the requested nodes, initializing them on demand"""
        if not types:
            return {}
        
        print(f"Initializing requested nodes: {types}")
        return {
            node_type: self._node_mapping[node_type]
            for node_type in types
            if node_type in self._node_mapping
        }
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate node condition"""
        nodes = self.get_items_by_types(types=[NodeType.AGENT])  # Default to agent node
        if nodes:
            node_handler = next(iter(nodes.values()))
            return node_handler(state)
        return "generate"  # Default fallback