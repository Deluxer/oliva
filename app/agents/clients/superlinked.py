from app.agents.schema.superlinked import index
import superlinked.framework as sl
from app.agents.config.qdrant import qdrant_config
from typing import Optional
import logging

class QdrantConnectionError(Exception):
    pass

class SuperlinkedClient:
    def __init__(self) -> None:
        self.app = None

    def setup(self):
        self.app: Optional[sl.InteractiveExecutor] = None
        try:
            product_source: sl.InteractiveSource = sl.InteractiveSource(index.product)

            vector_database = sl.QdrantVectorDatabase(
                url=qdrant_config.QDRANT_URL.get_secret_value(),
                api_key=qdrant_config.QDRANT_API_KEY.get_secret_value(),
                default_query_limit=10,
            )     

            executor = sl.InteractiveExecutor(
                sources=[product_source],
                indices=[index.product_index],
                vector_database=vector_database,
            )
            self.app = executor.run()
        except Exception as e:
            logging.error(f"Failed to connect to Qdrant: {str(e)}")
            raise QdrantConnectionError("Failed to establish connection with Qdrant vector database. Please check your connection and credentials.") from e

superlinked = SuperlinkedClient()