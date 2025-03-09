
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class QdrantConfig(BaseSettings):
    """Qdrant client settings."""
    QDRANT_URL: SecretStr
    QDRANT_API_KEY: SecretStr
    QDRANT_COLLECTION_NAME: str = "amazon_products"
    QDRANT_VECTOR_DIMENSION: int = 2054
    QDRANT_VECTOR_NAME: str = "7df9fa23a0651b43"
    QDRANT_VECTOR_DISTANCE: str = "Dot"

qdrant_config = QdrantConfig()