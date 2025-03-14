from enum import Enum

class EdgeType(Enum):
    GRADE_DOCUMENTS = "grade_documents"
    CHECK_RELEVANCE = "check_relevance"

class NodeType(Enum):
    AGENT = "agent"
    GENERATE = "generate"
    REWRITE = "rewrite"
    SUPERVISOR = "supervisor"

class ToolType(Enum):
    BLOG_SEARCH = "blog_search"
    BLOG_ADVANCE_SEARCH = "blog_advance_search"
    BLOG_SUMMARY = "blog_summary"
    AMAZON_PRODUCTS_SEARCH_BY_JSON = "amazon_products_search_by_json"
    AMAZON_PRODUCTS_SEARCH_BY_SUPERLINKED = "amazon_products_search_by_superlinked"