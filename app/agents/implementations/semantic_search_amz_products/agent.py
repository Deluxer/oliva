from app.agents.core.base_agent import BaseAgent
from app.utils.types import ToolType, EdgeType, NodeType

class SemanticSearchAmazonProductsAgent(BaseAgent):
    """Agent specialized in searching amazon products"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.AMAZON_PRODUCTS_SEARCH],
            edge_types=[EdgeType.GRADE_DOCUMENTS, EdgeType.CHECK_RELEVANCE],
            node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
        )
    
    def process(self):
        # You can make this dynamic by accepting user input
        result = self.process_input({
            "query": "Find books under $20",
            "filters": {
                "category": 'Books'
            }
        })
        return result