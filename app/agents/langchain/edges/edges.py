from typing import Any, Dict, Literal
from app.utils.types import EdgeType
from app.agents.langchain.interface.base_provider import BaseProvider
from app.agents.langchain.edges.grade_documents import grade_documents
from app.agents.langchain.edges.check_relevance import check_relevance

class EdgeProvider(BaseProvider[EdgeType]):
    """Edge provider for blog post related operations"""
    
    def __init__(self):
        self._edge_mapping = {
            EdgeType.GRADE_DOCUMENTS: grade_documents,
            EdgeType.CHECK_RELEVANCE: check_relevance,
        }
        super().__init__()
    
    def _initialize_items(self) -> None:
        """Initialize edges by copying from edge mapping"""
        self._items = self._edge_mapping.copy()

    def get_items(self) -> Dict[EdgeType, Any]:
        """Get all edges"""
        return self._items
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        edges = self.get_items_by_types(types=[EdgeType.GRADE_DOCUMENTS])
        if edges:
            edge_handler = next(iter(edges.values()))
            return edge_handler(state)
        # Fallback if no edges found
        return "generate"
