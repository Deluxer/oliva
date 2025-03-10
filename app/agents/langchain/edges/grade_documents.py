from typing import Literal
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants
from app.utils.prompts import prompts

def grade_documents(state: AgentState) -> Literal["generate", "rewrite"]:
    """Determines whether the retrieved documents are relevant to the question."""
    class grade(BaseModel):
        """Binary score for relevance check."""
        binary_score: str = Field(description="Relevance score 'yes' or 'no'")
        explanation: str = Field(description="Brief explanation of the relevance decision")

    model = ChatOpenAI(temperature=0, model=constants.LLM_MODEL, streaming=True)
    llm_with_tool = model.with_structured_output(grade)

    prompt = PromptTemplate(
        template=prompts.GRADE_DOCUMENTS_PROMPT_OPT_2,
        input_variables=["context", "question"],
    )

    chain = prompt | llm_with_tool
    messages = state["messages"]
    question = messages[0].content
    docs = messages[-1].content
    
    rewrite_count = state["rewrite_count"]
    
    # Define a max rewrite limit to avoid infinite loops
    MAX_REWRITE_ATTEMPTS = 2

    scored_result = chain.invoke({"question": question, "context": docs})
    
    if scored_result.binary_score == "yes":
        return "generate"
    else:
        state["rewrite_count"] = rewrite_count + 1
        state["explanation"] = scored_result.explanation

        # Stop rewriting after max attempts
        if state["rewrite_count"] >= MAX_REWRITE_ATTEMPTS:
            return "generate"

    return "rewrite"
