from langchain_core.tools import tool
from app.agents.langchain.vector_store.url_retriever import url_retriever

@tool('blog_search', description="Searching information in blog posts.")
def search_in_blog_posts_tool(query: str):
    """Create and return a blog post search tool"""
    retriever = url_retriever()
    docs = retriever.invoke(query)
    doc_txt = docs[0].page_content
    return doc_txt

@tool('blog_advance_search', description="Tool for searching blog posts based on a user's query.")
def search_in_blog_posts_tool_advance(query: str):
    """Create and return an advanced blog post search tool"""
    pass

@tool('blog_summary', description="Tool for searching blog posts based on a user's query.")
def search_in_blog_posts_tool_summary(query: str):
    """Create and return a blog post summary tool"""
    pass