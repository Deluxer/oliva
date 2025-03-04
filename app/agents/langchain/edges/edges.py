from typing import Any, Dict, List, Literal
from app.utils.types import EdgeType
from app.agents.langchain.base.edges import BaseEdgeCondition
from app.agents.langchain.edges.grade_documents import grade_documents
from app.agents.langchain.edges.check_relevance import check_relevance

class EdgeProvider(BaseEdgeCondition):
    """Edge provider for blog post related operations"""
    
    def __init__(self):
        self._initialize_edges()
    
    def _initialize_edges(self):
        """Initialize available edges"""
        self._edges = {
            EdgeType.GRADE_DOCUMENTS: grade_documents,
            EdgeType.CHECK_RELEVANCE: check_relevance,
        }
    
    def get_edges(self) -> Dict[EdgeType, Any]:
        """Get all available edges"""
        return self._edges
    
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state using the appropriate edge condition"""
        # Get the first available edge handler
        if self._edges:
            edge_handler = next(iter(self._edges.values()))
            return edge_handler(state)
        return "generate"  # Default fallback