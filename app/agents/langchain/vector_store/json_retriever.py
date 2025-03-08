import json
import os
from pathlib import Path
import pprint
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

from app.utils.constants import constants

load_dotenv()

def json_retriever():
    """Setup and return the document retriever"""
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create persistent directory for Chroma
    persist_dir = data_dir / "chroma_db"
    persist_dir.mkdir(exist_ok=True)
    
    # Check if dataset exists
    if not constants.PROCESSED_DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {constants.PROCESSED_DATASET_PATH}. Please ensure the file exists.")
    
    docs = []
    seen_titles = set()  # Track seen titles to avoid duplicates
    
    with open(constants.PROCESSED_DATASET_PATH, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                data = json.loads(line)
                title = data.get('title', '')
                
                # Skip if we've seen this title before
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                
                # Handle price that could be string or float
                price_raw = data.get('price', 0)
                if isinstance(price_raw, str):
                    price_str = price_raw.replace('$', '').replace(',', '')
                    try:
                        price = float(price_str)
                    except ValueError:
                        price = 0.0
                else:
                    price = float(price_raw)
                
                # Convert category list to string if it exists
                category = data.get('category', [])
                category_str = ', '.join(category) if isinstance(category, list) else str(category)
                
                # Create a rich page content that includes price for better matching
                page_content = f"Title: {title}. Price: ${price:.2f} Category: {category_str} rating: {data.get('review_rating', '')}"
                
                docs.append(Document(
                    page_content=page_content,
                    metadata={
                        'title': title,
                        'price': price,  # Store as float for easy comparison
                        'type': data.get('type', ''),
                        'category': category_str,
                        'rating': data.get('review_rating', ''),
                        'reviews': data.get('review_count', '')
                    }
                ))

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=constants.CHUNK_SIZE,
        chunk_overlap=constants.CHUNK_OVERLAP
    )
    doc_splits = text_splitter.split_documents(docs)

    # Use persistent storage for Chroma
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="amazon-products",
        embedding=OpenAIEmbeddings(model=constants.EMBEDDING_MODEL),
        #persist_directory=str(persist_dir)
    )
    return vectorstore.as_retriever()