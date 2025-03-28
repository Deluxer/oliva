from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from typing import List
from langchain_core.documents import Document

from app.utils.constants import constants

load_dotenv()

_retriever = None

def url_retriever():
    """Setup and return the document retriever"""
    global _retriever
    
    if _retriever is not None:
        return _retriever
    
    docs_list: List[Document] = []
    for url in constants.URLS:
        loader = WebBaseLoader(
            url,
            header_template={"User-Agent": "Mozilla/5.0"},
            verify_ssl=False
        )
        docs = loader.load()
        docs_list.extend(docs)

    vectorstore = Chroma.from_documents(
        documents=docs_list,
        embedding=OpenAIEmbeddings(
            model=constants.EMBEDDING_MODEL,
            dimensions=1536
        ),
    )
    
    # CONFIGURE RETRIEVER WITH IMPROVED SEARCH PARAMETERS
    _retriever = vectorstore.as_retriever(
        search_type="mmr",  # Use Maximum Marginal Relevance
        search_kwargs={
            "k": 4,  # Return top 4 most relevant chunks
            "lambda_mult": 0.7  # Balance between relevance and diversity
        }
    )
    
    return _retriever