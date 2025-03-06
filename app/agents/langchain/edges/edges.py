from typing import Any, Dict, List, Literal, Optional, Sequence
from app.utils.types import EdgeType
from app.agents.langchain.interface.base_provider import BaseProvider
from app.agents.langchain.edges.grade_documents import grade_documents
from app.agents.langchain.edges.check_relevance import check_relevance

class EdgeProvider(BaseProvider):
    """Edge provider for blog post related operations"""
    
    def __init__(self):
        self._edges = None
        self._edge_mapping = {
            EdgeType.GRADE_DOCUMENTS: grade_documents,
            EdgeType.CHECK_RELEVANCE: check_relevance,
        }
        super().__init__()
    
    def _initialize_items(self):
        """Initialize edges container"""
        if self._edges is None:
            self._edges = {}
    
    def get_items(self) -> Dict[EdgeType, Any]:
        """Get all edges"""
        self._initialize_items()
        return self._edges
    
    def get_items_by_types(self, types: Optional[Sequence[EdgeType]]) -> Dict[EdgeType, Any]:
        """Return only the requested edges, initializing them on demand"""
        if not types:
            return {}
        
        print(f"Initializing requested edges: {types}")
        return {
            edge_type: self._edge_mapping[edge_type]
            for edge_type in types
            if edge_type in self._edge_mapping
        }
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate edge condition"""
        edges = self.get_items_by_types(types=[EdgeType.GRADE_DOCUMENTS])  # Default to grade_documents
        if edges:
            edge_handler = next(iter(edges.values()))
            return edge_handler(state)
        return "generate"  # Default fallback