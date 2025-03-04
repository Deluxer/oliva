from langgraph.graph import StateGraph

class AgentFactory:
    @staticmethod
    def create_agent(workflow: StateGraph):
        return workflow.compile()