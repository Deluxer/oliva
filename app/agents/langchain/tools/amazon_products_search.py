from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.config.json_retriever import setup_retriever

def search_products():
    """Create and return a blog post search tool"""
    retriever = setup_retriever()
    return create_retriever_tool(
        retriever,
        name="search_products",
        description="Search for products on Amazon",
    )