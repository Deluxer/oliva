from langchain_core.tools import tool
from app.agents.langchain.vector_store.json_retriever import json_retriever
from app.agents.langchain.vector_store.sl_amazon_products_retriever import superlinked_amazon_products_retriever
from langchain_core.messages import AIMessage

@tool('search_products_by_json', description="Tool for searching products based on a user's query.")
def by_json(query: str):
    """Search for Amazon products using JSON data"""
    retriever = json_retriever()
    docs = retriever.invoke(query)
    doc_txt = docs[1].page_content
    return AIMessage(content=doc_txt)

@tool('search_products_by_superlinked', description="Tool for searching products based on a user's query.")
def by_superlinked(query: str):
    """Search for Amazon products using Superlinked"""
    return superlinked_amazon_products_retriever(query)