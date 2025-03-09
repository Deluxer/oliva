from typing import Any, Dict, Literal, Optional, Sequence
from app.utils.types import NodeType
from app.agents.langchain.interface.base_provider import BaseProvider
from app.agents.langchain.nodes.agent import agent
from app.agents.langchain.nodes.generate import generate
from app.agents.langchain.nodes.rewrite import rewrite

class NodeProvider(BaseProvider[NodeType]):
    """Node provider for blog post related operations"""
    def __init__(self):
        self._node_mapping = {
            NodeType.AGENT: agent,
            NodeType.GENERATE: generate,
            NodeType.REWRITE: rewrite,
        }
        super().__init__()
    
    def _initialize_items(self) -> None:
        """Initialize nodes by copying from node mapping"""
        self._items = self._node_mapping.copy()

    def get_items(self) -> Dict[NodeType, Any]:
        """Get all nodes"""
        return self._items
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate node condition"""
        nodes = self.get_items_by_types(types=[NodeType.GENERATE])
        if nodes:
            node_handler = next(iter(nodes.values()))
            return node_handler(state)
        # Fallback if no nodes found
        return "generate"