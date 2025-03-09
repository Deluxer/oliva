from app.agents.schema.superlinked import index
import superlinked.framework as sl

from app.agents.config.qdrant import qdrant_config

class SuperlinkedClient:
    def __init__(self):
        self.product_source: sl.InteractiveSource = sl.InteractiveSource(index.product)

        self.vector_database = sl.QdrantVectorDatabase(
            url=qdrant_config.QDRANT_URL.get_secret_value(),
            api_key=qdrant_config.QDRANT_API_KEY.get_secret_value(),
            default_query_limit=10,
        )     

        executor = sl.InteractiveExecutor(
            sources=[self.product_source],
            indices=[index.product_index],
            vector_database=self.vector_database,
        )
        self.app = executor.run()