
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class QdrantConfig(BaseSettings):
    """Qdrant client settings."""
    # superlinked
    QDRANT_URL: SecretStr
    QDRANT_API_KEY: SecretStr
    QDRANT_VECTOR_DIMENSION: int = 2054
    QDRANT_VECTOR_DISTANCE: str = "Dot"
    # long term memory
    QDRANT_COLLECTION_NAME: str = "oliva_history"
    QDRANT_VECTOR_NAME: str = "history_vector"

qdrant_config = QdrantConfig()