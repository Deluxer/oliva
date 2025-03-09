from app.utils.types import ToolType
from langchain.tools.retriever import create_retriever_tool
from app.agents.langchain.vector_store.url_retriever import url_retriever
from langchain_core.prompts import PromptTemplate

# Define a simple document prompt that returns just the content
# document_prompt = PromptTemplate(
#     input_variables=["page_content"],
#     template="{page_content}"
# )

def search_in_blog_posts_tool():
    """Create and return a blog post search tool"""
    tool = create_retriever_tool(
        retriever=url_retriever(),
        name=ToolType.BLOG_SEARCH,
        description="Search information in blog posts.",
        # document_prompt=document_prompt
    )
    return tool

def search_in_blog_posts_tool_one():
    """Create and return an advanced blog post search tool"""
    pass

def search_in_blog_posts_tool_two():
    """Create and return a blog post summary tool"""
    pass