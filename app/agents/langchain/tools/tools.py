from typing import Any, Dict
import logging
from importlib import import_module
from app.agents.langchain.interface.base_provider import BaseProvider
from app.utils.types import ToolType

logger = logging.getLogger(__name__)

class ToolProvider(BaseProvider[ToolType]):
    """Provider for all available tools"""

    def __init__(self):
        self._tool_imports: Dict[ToolType, tuple[str, str]] = {
            ToolType.BLOG_SEARCH: ("app.agents.langchain.tools.blog_posts", "search_in_blog_posts_tool"),
            ToolType.BLOG_ADVANCE_SEARCH: ("app.agents.langchain.tools.blog_posts", "search_in_blog_posts_tool_advance"),
            ToolType.BLOG_SUMMARY: ("app.agents.langchain.tools.blog_posts", "search_in_blog_posts_tool_summary"),
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_JSON: ("app.agents.langchain.tools.amazon_products_search", "by_json"),
            ToolType.AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED: ("app.agents.langchain.tools.amazon_products_search", "by_superlinked"),
        }
        super().__init__()

    def _initialize_items(self) -> None:
        """Initialize tools lazily by storing function names without calling them"""
        self._items = {}

        for tool_type, (module_path, func_name) in self._tool_imports.items():
            try:
                module = import_module(module_path)
                self._items[tool_type] = getattr(module, func_name)
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to import tool {tool_type}: {e}")

    def get_items(self) -> Dict[ToolType, Any]:
        """Get all tools (as function references, not executed)"""
        return self._items
