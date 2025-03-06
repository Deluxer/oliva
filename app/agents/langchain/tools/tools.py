from typing import Any, Dict, Optional, Sequence
from app.agents.langchain.interface.base_provider import BaseProvider
from app.utils.types import ToolType
from .amazon_products_search import by_json, by_superlinked
from .blog_posts import (
    search_in_blog_posts_tool,
    search_in_blog_posts_tool_one,
    search_in_blog_posts_tool_two,
)

class ToolProvider(BaseProvider):
    """Provider for all available tools"""
    def __init__(self):
        self._tools = None
        self._tool_mapping = {
            ToolType.BLOG_SEARCH: search_in_blog_posts_tool,
            ToolType.BLOG_ADVANCE_SEARCH: search_in_blog_posts_tool_one,
            ToolType.BLOG_SUMMARY: search_in_blog_posts_tool_two,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON: by_json,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED: by_superlinked,
        }
        super().__init__()

    def _initialize_items(self):
        """Initialize tools by getting tools from each function"""
        if self._tools is None:
            self._tools = {}

    def get_items(self) -> Dict[ToolType, Any]:
        """Get all tools"""
        self._initialize_items()
        return self._tools
    
    def get_items_by_types(self, types: Optional[Sequence[ToolType]]) -> Dict[ToolType, Any]:
        """Return only the requested tools, initializing them on demand"""
        if not types:
            return {}
        
        print(f"Initializing requested tools: {types}")
        return {
            tool_type: self._tool_mapping[tool_type]()
            for tool_type in types
            if tool_type in self._tool_mapping
        }