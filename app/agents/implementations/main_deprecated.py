from typing import Dict, Type
from agents.base.agent import BaseAgent
from agents.blog_post.agent import BlogPostAgent

class CallAgent:
    """Factory for creating different types of agents"""
    
    _agents: Dict[str, Type[BaseAgent]] = {
        "blog_search": BlogPostAgent,
        # Add more agents here as they are implemented
    }
    
    @classmethod
    def create_agent(cls, agent_type: str) -> BaseAgent:
        """Create an agent instance based on the specified type"""
        if agent_type not in cls._agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return cls._agents[agent_type]()

def process_query(agent_type: str, query: str) -> Dict:
    """Process a query using the specified agent type"""
    agent = CallAgent.create_agent(agent_type)
    return agent.process_input({"query": query})

def get_blog_posts():
    return process_query("blog_search", "How Harrison Chase defines an agent?")