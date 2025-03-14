from typing import Any, Dict
import logging
from app.agents.langchain.interface.base_provider import BaseProvider
from app.utils.types import ToolType

# Explicitly import tool functions instead of using import_module
from app.agents.langchain.tools.blog_posts import (
    search_in_blog_posts_tool,
    search_in_blog_posts_tool_advance,
    search_in_blog_posts_tool_summary,
)
from app.agents.langchain.tools.amazon_products_search import (
    by_json,
    by_superlinked,
)

class ToolProvider(BaseProvider[ToolType]):
    """Provider for all available tools"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Store function references directly instead of module paths
        self._tool_imports: Dict[ToolType, Any] = {
            ToolType.BLOG_SEARCH: search_in_blog_posts_tool,
            ToolType.BLOG_ADVANCE_SEARCH: search_in_blog_posts_tool_advance,
            ToolType.BLOG_SUMMARY: search_in_blog_posts_tool_summary,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON: by_json,
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED: by_superlinked,
        }
        super().__init__()
        self._initialized = True

    def _initialize_items(self) -> None:
        """Initialize tools lazily by storing function references"""
        self._items = self._tool_imports.copy()

    def get_items(self) -> Dict[ToolType, Any]:
        """Get all tools (as function references, not executed)"""
        return self._items
