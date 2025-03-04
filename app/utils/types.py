from enum import Enum

class EdgeType(Enum):
    GRADE_DOCUMENTS = "grade_documents"
    CHECK_RELEVANCE = "check_relevance"

class NodeType(Enum):
    AGENT = "agent"
    GENERATE = "generate"
    REWRITE = "rewriter"  

class ToolType(Enum):
    BLOG_SEARCH = "blog_search"
    BLOG_ADVANCE_SEARCH = "blog_advance_search"
    BLOG_SUMMARY = "blog_summary"
    AMAZON_PRODUCTS_SEARCH = "amazon_products_search"