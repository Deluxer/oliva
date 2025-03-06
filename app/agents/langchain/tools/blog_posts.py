from app.agents.langchain.vector_store.url_retriever_1 import url_retriever_one
from app.agents.langchain.vector_store.url_retriever_2 import url_retriever_two
from app.utils.types import ToolType
from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.vector_store.url_retriever import url_retriever

def search_in_blog_posts_tool():
    """Create and return a blog post search tool"""
    retriever = url_retriever()
    return create_retriever_tool(
        retriever,
        name=ToolType.BLOG_SEARCH,
        description="Search and return information about Harrison Chase blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
    )

def search_in_blog_posts_tool_one():
    """Create and return an advanced blog post search tool"""
    retriever = url_retriever_one()
    return create_retriever_tool(
        retriever,
        name=ToolType.BLOG_ADVANCE_SEARCH,
        description="Search and return information about Harrison Chase blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
    )

def search_in_blog_posts_tool_two():
    """Create and return a blog post summary tool"""
    retriever = url_retriever_two()
    return create_retriever_tool(
        retriever,
        name=ToolType.BLOG_SUMMARY,
        description="Find and summarize key points from Harrison Chase's blog posts about agent concepts and definitions.",
    )