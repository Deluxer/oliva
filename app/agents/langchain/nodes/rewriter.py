from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Dict, Any

from app.utils.constants import constants

def rewrite(state: Dict[str, Any]) -> Dict[str, Any]:
    """Transform the query to produce a better question"""
    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content
    rewrite_count = state.get("rewrite_count", 0)

    # Adjust strategy based on rewrite attempts
    if rewrite_count == 0:
        strategy = "Make the question more specific and focused on Harrison Chase's definition or explanation of agents in the context of LLMs or AI"
    else:
        strategy = "Broaden the question to look for any content about agents, LLMs, or AI systems in general"

    msg = [
        HumanMessage(
            content=f"""Task: Transform this question to get better search results.

Original question: {question}

Strategy: {strategy}

Requirements:
1. Maintain the core intent of finding information about agents
2. Focus on Harrison Chase's blog posts and writings
3. Consider both technical and conceptual aspects
4. Make the question more searchable

Provide only the rewritten question, no explanations."""
        )
    ]

    model = ChatOpenAI(temperature=0, model=constants.LLM_MODEL, streaming=True)
    response = model.invoke(msg)
    
    # Preserve the rewrite count in state
    return {
        "messages": [response],
        "rewrite_count": rewrite_count
    }