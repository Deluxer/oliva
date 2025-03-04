from pathlib import Path

class Constants:
    """Constants for LangChain integration"""
    # Configuration constants
    CHUNK_SIZE = 100
    CHUNK_OVERLAP = 50
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"

    # URLs for document loading
    URLS = [
        "https://blog.langchain.dev/what-is-an-agent/",
    ]
    PROCESSED_DATASET_PATH: Path = (
        Path("data") / "processed_100_sample.jsonl"
    )

# Create a singleton instance
constants = Constants()