from app.agents.langchain.vector_store.json_retriever import json_retriever
from app.agents.langchain.vector_store.sl_amazon_products_retriever import superlinked_amazon_products_retriever
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import Tool

def by_json():
    """Search for Amazon products using JSON data"""
    return create_retriever_tool(
        retriever=json_retriever(),
        name="search_products_by_json",
        description="Search for products.Input should be a natural language query describing what you're looking for, including any specific requirements about, title, price, category, rating, reviews, or features.",
    )

def by_superlinked():
    """Search for Amazon products using Superlinked"""
    return Tool(
        func=superlinked_amazon_products_retriever,
        name="search_products_by_superlinked",
        description="Search for products.Input should be a natural language query describing what you're looking for, including any specific requirements about, title, price, category, rating, reviews, or features.",
    )