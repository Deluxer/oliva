from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.utils.types import ToolType
from typing import Any, Dict

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    rewrite_count: int
    tools: list[ToolType]
    explanation: str