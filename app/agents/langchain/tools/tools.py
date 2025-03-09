from typing import Any, Dict
from app.agents.langchain.interface.base_provider import BaseProvider
from app.utils.types import ToolType
from .amazon_products_search import by_json, by_superlinked
from .blog_posts import (
    search_in_blog_posts_tool,
    search_in_blog_posts_tool_one,
    search_in_blog_posts_tool_two,
)

class ToolProvider(BaseProvider[ToolType]):
    """Provider for all available tools"""
    def __init__(self):
        self._tool_mapping = {
            ToolType.BLOG_SEARCH: search_in_blog_posts_tool,
            ToolType.BLOG_ADVANCE_SEARCH: search_in_blog_posts_tool_one,
            ToolType.BLOG_SUMMARY: search_in_blog_posts_tool_two,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON: by_json,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED: by_superlinked,
        }
        super().__init__()

    def _initialize_items(self) -> None:
        """Initialize tools by copying from tool mapping"""
        self._items = self._tool_mapping.copy()

    def get_items(self) -> Dict[ToolType, Any]:
        """Get all tools"""
        return self._items