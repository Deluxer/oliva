from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Sequence

from app.utils.types import EdgeType

class BaseEdgeCondition(ABC):
    """Abstract base class for edge conditions"""
    
    def __init__(self):
        self._edges: Dict[EdgeType, Any] = {}
        self._initialize_edges()
    
    @abstractmethod
    def _initialize_edges(self):
        """Initialize available edges"""
        pass
    
    @abstractmethod
    def get_edges(self) -> Dict[EdgeType, Any]:
        """Get all available edges mapped by their types"""
        pass
    
    def get_edges_by_types(self, edge_types: Optional[Sequence[EdgeType]]) -> List[Any]:
        """Get specific edges by their types"""
        edges_dict = self.get_edges()
        # If no types specified, return all edges
        if not edge_types:
            return list(edges_dict.values())
            
        selected_edges = []
        for edge_type in edge_types:
            if edge_type in edges_dict:
                selected_edges.append(edges_dict[edge_type])
        return selected_edges
    
    @abstractmethod 
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state and return next node"""
        pass