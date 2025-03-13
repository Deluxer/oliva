from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

from app.utils.constants import constants

load_dotenv()

# Cache the retriever instance
_retriever = None

def url_retriever():
    """Setup and return the document retriever"""
    global _retriever
    
    if _retriever is not None:
        return _retriever
        
    docs = [WebBaseLoader(url).load() for url in constants.URLS]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=constants.CHUNK_SIZE,
        chunk_overlap=constants.CHUNK_OVERLAP
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Create vectorstore and initialize retriever
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        # collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(model=constants.EMBEDDING_MODEL),
    )
    
    # Cache and return the retriever
    _retriever = vectorstore.as_retriever()
    return _retriever