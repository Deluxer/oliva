from typing import Any, List, Type, Union
from app.agents.langchain.interface.base_provider import BaseProvider
from langgraph.prebuilt import ToolNode
class AgentEvents:
    @staticmethod
    def mapper(
        tools: Union[List[Any], Type[BaseProvider]],
        edges: Union[List[Any], Type[BaseProvider]],
        nodes: Union[List[Any], Type[BaseProvider]],
    ) -> List[Any]:
        # Initialize tools - handle both instances and provider classes
        tool_list = tools() if isinstance(tools, type) else tools
        if isinstance(tool_list, list):
            retriever_tool = ToolNode(tool_list)
        else:
            # If it's a dictionary, get the values
            retriever_tool = ToolNode(list(tool_list.values()))

        return [retriever_tool, edges, nodes]