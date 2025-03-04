from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Sequence

from app.utils.types import NodeType

class BaseNodesProvider(ABC):
    """Abstract base class for nodes providers"""
    
    def __init__(self):
        self._nodes: Dict[NodeType, Any] = {}
        self._initialize_nodes()
    
    @abstractmethod
    def _initialize_nodes(self):
        """Initialize available nodes"""
        pass
    
    @abstractmethod
    def get_nodes(self) -> Dict[NodeType, Any]:
        """Get all available nodes mapped by their types"""
        pass
    
    def get_nodes_by_types(self, node_types: Optional[Sequence[NodeType]]) -> List[Any]:
        """Get specific nodes by their types"""
        nodes_dict = self.get_nodes()
        # If no types specified, return all nodes
        if not node_types:
            return list(nodes_dict.values())
            
        selected_nodes = {}
        for node_type in node_types:
            if node_type in nodes_dict:
                selected_nodes[node_type] = nodes_dict[node_type]
        return selected_nodes
    
    @abstractmethod 
    def evaluate(self, state: Any) -> Literal["generate", "rewrite", str]:
        """Evaluate the state and return next node"""
        pass