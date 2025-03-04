
from typing import Any, List, Type
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.utils.constants import constants
from app.agents.langchain.state import AgentState

class LangChainTemplate:
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