from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence

from app.utils.types import ToolType

class BaseToolProvider(ABC):
    """Base class for tool providers"""
    
    def __init__(self):
        self._tools: Dict[ToolType, Any] = {}
        self._initialize_tools()
    
    @abstractmethod
    def _initialize_tools(self):
        """Initialize available tools"""
        pass
    
    @abstractmethod
    def get_tools(self) -> Dict[ToolType, Any]:
        """Get all available tools mapped by their types"""
        pass

    def get_tools_by_types(self, tool_types: Optional[Sequence[ToolType]]) -> List[Any]:
        """Get specific tools by their types"""
        tools_dict = self.get_tools()
        if not tool_types:  # If no types specified, return all tools
            return list(tools_dict.values())
            
        selected_tools = []
        for tool_type in tool_types:
            if tool_type in tools_dict:
                selected_tools.append(tools_dict[tool_type])
        return selected_tools
    
    def get_tool(self, tool_type: ToolType) -> Optional[Any]:
        """Get a specific tool by type"""
        return self._tools.get(tool_type)
    
    def get_available_tools(self) -> List[ToolType]:
        """Get list of available tool types"""
        return list(self._tools.keys())