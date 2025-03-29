from typing import Annotated, Sequence
from langgraph.graph import MessagesState
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.utils.types import ToolType
import operator

def last_value_reducer(current: str | None, new: str) -> str:
    """Reducer that keeps only the last value, preserving initial value if new is empty"""
    if new == "":
        return current if current is not None else ""
    return new

class BaseState(MessagesState):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next: Annotated[str, last_value_reducer]

class AgentState(BaseState):
    pass

class SubGraphAgentState(BaseState):
    rewrite_count: Annotated[int, operator.add]
    tools: Annotated[list[ToolType], operator.add]
    explanation: Annotated[str, operator.add]