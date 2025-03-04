from typing import Dict, Optional, Sequence
from app.utils.types import ToolType
from .blog_posts import (
    search_in_blog_posts_tool,
    search_in_blog_posts_tool_2,
    search_in_blog_posts_tool_3,
)
from .amazon_products_search import search_products

class BaseToolProvider:
    """Base class for tool providers"""
    def __init__(self):
        self._tools = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize the tools dictionary. Must be implemented by subclasses."""
        raise NotImplementedError
    
    def get_tools_by_types(self, tool_types: Optional[Sequence[ToolType]] = None) -> Dict:
        """Get tools based on specified types or all available tools if none specified"""
        if not tool_types:
            return self._tools
        return {t: self._tools[t] for t in tool_types if t in self._tools}

class ToolProvider(BaseToolProvider):
    """Tool provider for blog post related operations"""
    def _initialize_tools(self):
        """Initialize tools by getting tools from each function"""
        self._tools = {
            ToolType.BLOG_SEARCH: search_in_blog_posts_tool(),
            ToolType.BLOG_ADVANCE_SEARCH: search_in_blog_posts_tool_2(),
            ToolType.BLOG_SUMMARY: search_in_blog_posts_tool_3(),
            ToolType.AMAZON_PRODUCTS_SEARCH: search_products(),
        }