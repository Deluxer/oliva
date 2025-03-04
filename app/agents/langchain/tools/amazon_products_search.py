from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.vector_store.json_retriever import json_retriever

def search_products():
    """Create and return a blog post search tool"""
    retriever = json_retriever()
    return create_retriever_tool(
        retriever,
        name="search_products",
        description="Search for products on Amazon",
    )