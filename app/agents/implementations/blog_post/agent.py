from app.agents.core.agent_state import AgentState
from app.agents.core.base_agent import BaseAgent
from app.utils.types import EdgeType, NodeType, ToolType
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from app.agents.langchain.factory import AgentFactory
from typing import Dict, Any

class BlogPostAgent(BaseAgent):
    """Agent specialized in searching and analyzing blog posts"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__(
                tool_types=[ToolType.BLOG_SEARCH],
                edge_types=[EdgeType.GRADE_DOCUMENTS],
                node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
            )
            self._initialized = True
            self._workflow = None
    
    def prepare(self):
        """Prepare the agent workflow only when needed"""
        if self._workflow is None:
            self._workflow = StateGraph(AgentState)
            events = self.setup_events()
            tools, edges, nodes = events
            # Dynamic injection of tools into the agent node
            agent = self.inject_tools_in_node(tools, nodes[NodeType.AGENT])

            self._workflow.add_node("agent", agent)
            self._workflow.add_node("retrieve", ToolNode(tools))
            self._workflow.add_node("rewrite", nodes[NodeType.REWRITE])
            self._workflow.add_node("generate", nodes[NodeType.GENERATE])
            self._workflow.add_edge(START, "agent")
            self._workflow.add_conditional_edges(
                "agent",
                tools_condition,
                {"tools": "generate", END: END}
            )
            self._workflow.add_conditional_edges(
                "generate",
                edges[EdgeType.GRADE_DOCUMENTS],
                {"generate": "generate", "rewrite": "rewrite"}
            )
            self._workflow.add_edge("generate", END)
            self._workflow.add_edge("rewrite", "agent")

    def process(self, input_state: Dict[str, Any]) -> Dict[str, Any]:
        self.prepare()
        return AgentFactory.create_agent(self._workflow, input_state)

    def studio(self) -> Dict[str, Any]:
        """Compile workflow for LangGraph Studio"""
        self.prepare()
        return self._workflow.compile()

agent = BlogPostAgent()

# Initialize graph for LangGraph Studio
graph = agent.studio()