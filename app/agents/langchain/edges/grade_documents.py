from typing import Literal
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.utils.constants import constants
from app.utils.prompts import prompts

def grade_documents(state) -> Literal["generate", "rewrite"]:
    """Determines whether the retrieved documents are relevant to the question."""
    print("---GRADE DOCUMENTS---")

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

    # Initialize rewrite_count in state if not present
    if "rewrite_count" not in state:
        state["rewrite_count"] = 0
    
    rewrite_count = state["rewrite_count"]
    
    # Define a max rewrite limit to avoid infinite loops
    MAX_REWRITE_ATTEMPTS = 2  # Adjust as needed

    scored_result = chain.invoke({"question": question, "context": docs})
    
    if scored_result.binary_score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"
    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(f"Explanation: {scored_result.explanation}")
        state["rewrite_count"] = rewrite_count + 1

        # Stop rewriting after max attempts
        if state["rewrite_count"] >= MAX_REWRITE_ATTEMPTS:
            print(f"---MAX REWRITE ATTEMPTS REACHED ({MAX_REWRITE_ATTEMPTS})---")
            return "generate"  # Prevent infinite loop

    return "rewrite"
