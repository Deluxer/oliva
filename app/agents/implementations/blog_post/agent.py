from app.agents.core.base_agent import BaseAgent
from app.agents.langchain.base.tools import ToolType
from app.agents.langchain.base.edges import EdgeType

class BlogPostAgent(BaseAgent):
    """Agent specialized in searching and analyzing blog posts"""
    
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.BLOG_SEARCH],
            edge_types=[EdgeType.AGENT, EdgeType.GENERATOR, EdgeType.REWRITE]
        )
    
    def process(self):
        result = self.process_input({"query": "How Harrison Chase defines an agent?"})
        return result