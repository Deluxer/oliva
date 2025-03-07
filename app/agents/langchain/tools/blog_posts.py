from app.agents.langchain.vector_store.url_retriever_1 import url_retriever_one
from app.agents.langchain.vector_store.url_retriever_2 import url_retriever_two
from app.utils.types import ToolType
from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.vector_store.url_retriever import url_retriever
from langchain_core.prompts import PromptTemplate

# Define a simple document prompt that returns just the content
document_prompt = PromptTemplate(
    input_variables=["page_content"],
    template="{page_content}"
)

def search_in_blog_posts_tool():
    """Create and return a blog post search tool"""
    tool = create_retriever_tool(
        retriever=url_retriever(),
        name=ToolType.BLOG_SEARCH,
        description="Search information in blog posts.",
        document_prompt=document_prompt
    )
    return tool

def search_in_blog_posts_tool_one():
    """Create and return an advanced blog post search tool"""
    return create_retriever_tool(
        retriever=url_retriever_one(),
        name=ToolType.BLOG_ADVANCE_SEARCH,
        description="Search information in blog posts.",
        document_prompt=document_prompt
    )

def search_in_blog_posts_tool_two():
    """Create and return a blog post summary tool"""
    return create_retriever_tool(
        retriever=url_retriever_two(),
        name=ToolType.BLOG_SUMMARY,
        description="Find and summarize key points from Harrison Chase's blog posts about agent concepts and definitions.",
        document_prompt=document_prompt
    )