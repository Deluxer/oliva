from app.agents.schema.superlinked import index
import superlinked.framework as sl

from app.utils.constants import constants

class SuperlinkedClient:
    def __init__(self):
        self.product_source: sl.InteractiveSource = sl.InteractiveSource(index.product)

        self.vector_database = sl.QdrantVectorDatabase(
            constants.QDRANT_DATABASE_URL,
            constants.QDRANT_DATABASE_API_KEY,
            default_query_limit=10,
        )     

        executor = sl.InteractiveExecutor(
            sources=[self.product_source],
            indices=[index.product_index],
            vector_database=self.vector_database,
        )
        self.app = executor.run()