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
        return [tools, edges, nodes]

    @staticmethod
    def transform(event_list: Union[List[Any], Type[BaseProvider]]) -> List[Any]:
        if isinstance(event_list, dict):
            # Call each function in the dictionary and collect results
            return ToolNode([func() for func in event_list.values()])

        if isinstance(event_list, list):
            # If it's a list, return as is
            return event_list

        if isinstance(event_list, type):
            # If it's a provider class, instantiate it
            return event_list()