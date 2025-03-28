from langchain_core.tools import tool
from app.agents.langchain.vector_store.url_retriever import url_retriever
from typing import List
from langchain_core.documents import Document

def format_search_results(docs: List[Document]) -> str:
    """Format search results in a clear and structured way"""
    if not docs:
        return "No relevant information found."
    
    # Remove duplicate content and sort by relevance
    seen_content = set()
    unique_docs = []
    
    for doc in docs:
        content = doc.page_content.strip()
        if content not in seen_content:
            seen_content.add(content)
            unique_docs.append(doc)
    
    formatted_results = []
    for doc in unique_docs:
        metadata = doc.metadata
        title = metadata.get('title', 'No title')
        source = metadata.get('source', 'No source')
        content = doc.page_content.strip()
        
        # Clean up content formatting
        content = content.replace('\n\t\n', '\n').replace('\n\n\n', '\n\n')
        content = content.replace('\t', '').strip()
        
        if content:  # Only include non-empty content
            result = f"Source: {source}\nTitle: {title}\nContent:\n{content}\n"
            formatted_results.append(result)
    
    return "\n---\n".join(formatted_results)

@tool('blog_search', description="Search for specific information in blog posts.")
def search_in_blog_posts_tool(query: str):
    """Search for relevant information in blog posts
    
    Args:
        query: The search query string
        
    Returns:
        Formatted string containing relevant blog post content
    """
    print("Search query:", query)
    retriever = url_retriever()
    docs = retriever.invoke(query)
    print("Retrieved docs from Vector Store:", len(docs), "results")
    return format_search_results(docs)

@tool('blog_advance_search', description="Advanced search in blog posts with metadata filtering.")
def search_in_blog_posts_tool_advance(query: str):
    """Advanced search in blog posts with metadata filtering"""
    # TODO: Implement advanced search with metadata filtering
    pass

@tool('blog_summary', description="Generate a concise summary of blog post search results.")
def search_in_blog_posts_tool_summary(query: str):
    """Generate a concise summary of blog post search results"""
    # TODO: Implement summary generation
    pass