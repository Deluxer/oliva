from app.agents.schema.superlinked import query_search
from langchain_core.messages import AIMessage
import logging

class SuperlinkedAmazonProductsRetriever:
    """Retrieves Amazon products based on a query using Superlinked"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = False
            self.client = None
            self._initialized = True
    
    def _ensure_client(self):
        """Lazy initialization of the client"""
        if self.client is None:
            try:
                from app.agents.clients.superlinked import superlinked
                self.client = superlinked
                return True
            except Exception as e:
                logging.error("Retriever init failed: %s", str(e))
                return False
        return True
    
    def get_products(self, query: str, limit: int = 3) -> str:
        if not self._ensure_client():
            return "Error: Qdrant connection failed"
        try:
            self.client.setup()
            result = self.client.app.query(
                query_search.semantic_query,
                natural_query=query,
                limit=limit
            )
            to_pandas = result.to_pandas()
            products = self._format_products(to_pandas)
            return "\n".join(products)
        except Exception as e:
            msg = f"Query failed: {e}"
            logging.error(msg)
            return msg
    
    def _format_products(self, df):
        products = []
        for _, row in df.iterrows():
            title = row["title"]
            price = f"${row['price']:.2f}"
            rating = f"{row['review_rating']} ({row['review_count']} reviews)"
            products.append(f"{title}\nPrice: {price}\nRating: {rating}\n")
        return products

retriever = SuperlinkedAmazonProductsRetriever()