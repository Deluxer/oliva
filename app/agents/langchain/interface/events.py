from typing import Any, List, Type, Union
from app.agents.core.agent_state import AgentState
from app.agents.langchain.interface.base_provider import BaseProvider
from langgraph.prebuilt import ToolNode

class AgentEvents:
    @staticmethod
    def mapper(
        tools: Union[List[Any], Type[BaseProvider]],
        edges: Union[List[Any], Type[BaseProvider]],
        nodes: Union[List[Any], Type[BaseProvider]],
    ) -> List[Any]:
        tools_list = list(tools.values())
        return [tools_list, edges, nodes]