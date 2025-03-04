from typing import Dict, Any, Literal
from langchain_core.messages import AIMessage

def check_relevance(state) -> Literal["generate", "rewrite"]:
    """Check relevance of retrieved documents."""
    print("---CHECK RELEVANCE---")
    
    messages = state["messages"]
    last_message = messages[-1]
    
    if not isinstance(last_message, AIMessage):
        raise ValueError("The 'checkRelevance' node requires the most recent message to be an AIMessage")
        
    if not hasattr(last_message, "tool_calls"):
        raise ValueError("The 'checkRelevance' node requires the most recent message to contain tool calls")
        
    tool_calls = last_message.tool_calls
    if not tool_calls or len(tool_calls) == 0:
        raise ValueError("Last message was not a function message")
    
    if tool_calls[0].args.get("binary_score") == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"
        
    print("---DECISION: DOCS NOT RELEVANT---")
    return "rewrite"