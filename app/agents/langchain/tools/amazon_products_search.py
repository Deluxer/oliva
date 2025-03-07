from app.agents.langchain.vector_store.json_retriever import json_retriever
from langchain.tools.retriever import create_retriever_tool

def by_json():
    """Search for Amazon products using JSON data"""
    retriever = json_retriever()
    return create_retriever_tool(
        retriever,
        name="search_products_by_json",
        description="Search for products.Input should be a natural language query describing what you're looking for, including any specific requirements about price, category, or features.",
    )

def by_superlinked():
    """Search for Amazon products using Superlinked"""
    retriever = json_retriever()
    return create_retriever_tool(
        retriever,
        name="search_products_by_superlinked",
        description="Search for products on Amazon using vector search. Input should be a natural language query describing what you're looking for.",
    )