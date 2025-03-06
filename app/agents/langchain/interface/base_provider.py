# Add type hints for better code clarity
from abc import abstractmethod
from typing import Dict, List, Optional, Sequence, Any, TypeVar, Generic

T = TypeVar('T')
class BaseProvider(Generic[T]):
    def __init__(self):
        self._items: Dict[T, Any] = {}
        self._initialize_items()
    
    @abstractmethod
    def _initialize_items(self) -> None:
        pass

    @abstractmethod
    def get_items(self) -> Dict[T, Any]:
        return self._items
    
    def get_items_by_types(self, types: Optional[Sequence[T]]) -> List[Any]:
        """Return items by types"""
        items_dict = self.get_items()
        # If no types specified, return all items
        if not types:
            return list(items_dict.values())
        
        selected_items = {}
        for item_type in types:
            if item_type in items_dict:
                selected_items[item_type] = items_dict[item_type]
        return selected_items