from typing import Any, Dict, List, Type, Union

from app.utils.types import NodeType, EdgeType
from .base.tools import BaseToolProvider
from .base.edges import BaseEdgeCondition
from .base.nodes import BaseNodesProvider
from app.agents.langchain.nodes.nodes import NodesProvider

from .state import AgentState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import END, StateGraph, START

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.utils.constants import constants

class AgentFactory:
    @staticmethod
    def create_agent(
        tools: Union[List[Any], Type[BaseToolProvider]],
        edges: Union[List[Any], Type[BaseEdgeCondition]],
        nodes: Union[List[Any], Type[BaseNodesProvider]],
    ):
        workflow = StateGraph(AgentState)
        
        # Initialize tools - handle both instances and provider classes
        tool_list = tools() if isinstance(tools, type) else tools
        if isinstance(tool_list, list):
            retrieve = ToolNode(tool_list)
        else:
            # If it's a dictionary, get the values
            retrieve = ToolNode(list(tool_list.values()))
        
        # Set up nodes
        nodes_dict = nodes().get_nodes() if isinstance(nodes, type) else {
            NodeType.AGENT: nodes[0],  # agent node
            NodeType.REWRITE: nodes[1],  # rewrite node
            NodeType.GENERATE: nodes[2],  # generate node
        }
        
        # Set up edges
        edges_dict = edges().get_edges() if isinstance(edges, type) else {
            EdgeType.GRADE_DOCUMENTS: edges[0],  # grade documents edge
            EdgeType.CHECK_RELEVANCE: edges[1],  # check relevance edge
        }

        workflow.add_edge(START, "agent")
        # Add nodes to workflow
        workflow.add_node("agent", nodes_dict[NodeType.AGENT])
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("rewrite", nodes_dict[NodeType.REWRITE])
        workflow.add_node("generate", nodes_dict[NodeType.GENERATE])
        
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "retrieve", END: END}
        )
        
        workflow.add_conditional_edges(
            "retrieve",
            edges_dict[EdgeType.GRADE_DOCUMENTS],
            {"generate": "generate", "rewrite": "rewrite"}
        )
        
        workflow.add_edge("generate", END)
        workflow.add_edge("rewrite", "agent")
        
        return workflow.compile()

class LangChainFactory:
    """Factory for creating LangChain components"""
    
    @staticmethod
    def create_llm(model_name: str = None, **kwargs) -> ChatOpenAI:
        """Create a ChatOpenAI instance with specified parameters"""
        return ChatOpenAI(
            temperature=kwargs.get('temperature', 0),
            model=model_name or constants.LLM_MODEL,
            streaming=kwargs.get('streaming', True)
        )
    
    @staticmethod
    def create_prompt(template: str, input_variables: List[str]) -> PromptTemplate:
        """Create a prompt template"""
        return PromptTemplate(
            template=template,
            input_variables=input_variables
        )
    
    @staticmethod
    def create_state() -> Type[AgentState]:
        """Create the agent state type"""
        return AgentState
    
    @staticmethod
    def create_chain(prompt: PromptTemplate, llm: ChatOpenAI, output_parser: Any = None):
        """Create a chain with the given components"""
        if output_parser:
            return prompt | llm | output_parser
        return prompt | llm