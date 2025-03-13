from typing import Any, Dict, Literal
import logging
from importlib import import_module
from app.utils.types import EdgeType
from app.agents.langchain.interface.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class EdgeProvider(BaseProvider[EdgeType]):
    """Edge provider for blog post related operations"""

    def __init__(self):
        self._edge_imports: Dict[EdgeType, tuple[str, str]] = {
            EdgeType.GRADE_DOCUMENTS: ("app.agents.langchain.edges.grade_documents", "grade_documents"),
        }
        super().__init__()

    def _initialize_items(self) -> None:
        """Lazy-load edges dynamically to prevent unnecessary imports."""
        self._items = {}

        for edge_type, (module_path, func_name) in self._edge_imports.items():
            try:
                module = import_module(module_path)
                self._items[edge_type] = getattr(module, func_name)
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to import edge {edge_type}: {e}")

    def get_items(self) -> Dict[EdgeType, Any]:
        """Get all edges"""
        return self._items

    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate edge condition"""
        edges = self.get_items()
        if EdgeType.GRADE_DOCUMENTS in edges:
            return edges[EdgeType.GRADE_DOCUMENTS](state)
        return "generate"  # Fallback
