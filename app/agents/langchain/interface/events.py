from typing import Any, List, Type, Union
from langgraph.prebuilt import ToolNode

from .tools import BaseToolProvider
from .edges import BaseEdgeCondition
from .nodes import BaseNodesProvider

class AgentEvents:
    @staticmethod
    def mapper(
        tools: Union[List[Any], Type[BaseToolProvider]],
        edges: Union[List[Any], Type[BaseEdgeCondition]],
        nodes: Union[List[Any], Type[BaseNodesProvider]],
    ) -> List[Any]:
        # Initialize tools - handle both instances and provider classes
        tool_list = tools() if isinstance(tools, type) else tools
        if isinstance(tool_list, list):
            retrieve = ToolNode(tool_list)
        else:
            # If it's a dictionary, get the values
            retrieve = ToolNode(list(tool_list.values()))

        return [retrieve, edges, nodes]