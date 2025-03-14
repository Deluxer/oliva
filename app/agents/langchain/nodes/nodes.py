from typing import Any, Dict, Literal
import logging
from importlib import import_module
from app.utils.types import NodeType
from app.agents.langchain.interface.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class NodeProvider(BaseProvider[NodeType]):
    """Node provider for blog post related operations"""

    def __init__(self):
        self._node_imports: Dict[NodeType, tuple[str, str]] = {
            NodeType.AGENT: ("app.agents.langchain.nodes.agent", "agent"),
            NodeType.GENERATE: ("app.agents.langchain.nodes.generate", "generate"),
            NodeType.REWRITE: ("app.agents.langchain.nodes.rewrite", "rewrite"),
            NodeType.SUPERVISOR: ("app.agents.langchain.nodes.supervisor", "supervisor"),
        }
        super().__init__()

    def _initialize_items(self) -> None:
        """Lazy-load nodes dynamically to prevent unnecessary imports."""
        self._items = {}

        for node_type, (module_path, func_name) in self._node_imports.items():
            try:
                module = import_module(module_path)
                self._items[node_type] = getattr(module, func_name)
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to import node {node_type}: {e}")

    def get_items(self) -> Dict[NodeType, Any]:
        """Get all nodes"""
        return self._items

    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate node condition"""
        nodes = self.get_items()
        if NodeType.GENERATE in nodes:
            return nodes[NodeType.GENERATE](state)
        return "generate"  # Fallback
