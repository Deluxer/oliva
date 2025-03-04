from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.vector_store.url_retriever import url_retriever

def search_in_blog_posts_tool():
    """Create and return a blog post search tool"""
    retriever = url_retriever()
    return create_retriever_tool(
        retriever,
        name="retrieve_blog_posts",
        description="Search for information in Harrison Chase's blog posts about LLM agents. Input should be a specific question about agents, LLMs, or AI systems.",
    )

def search_in_blog_posts_tool_2():
    """Create and return an advanced blog post search tool"""
    retriever = url_retriever()
    return create_retriever_tool(
        retriever,
        name="retrieve_advanced_blog_posts",
        description="Perform an advanced search in Harrison Chase's blog posts focusing on technical details about agent architectures and implementations.",
    )

def search_in_blog_posts_tool_3():
    """Create and return a blog post summary tool"""
    retriever = url_retriever()
    return create_retriever_tool(
        retriever,
        name="retrieve_blog_summaries",
        description="Find and summarize key points from Harrison Chase's blog posts about agent concepts and definitions.",
    )