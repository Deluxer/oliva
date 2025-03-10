from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain import hub

from app.agents.core.agent_state import AgentState
from app.utils.constants import constants
from app.utils.prompts import prompts

def generate(state: AgentState):
    """Generate answer based on retrieved documents"""
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]
    docs = last_message.content
    rewrite_count = state.get("rewrite_count", 0)

    # If we've tried rewriting and still found no results, generate a "no results" response
    if rewrite_count >= 1 and "DOCS NOT RELEVANT" in docs:
        no_results_prompt = PromptTemplate(
            template=prompts.NO_RESULTS_PROMPT,
            input_variables=["question"]
        )
        llm = ChatOpenAI(model_name=constants.LLM_MODEL, temperature=0, streaming=True)
        chain = no_results_prompt | llm | StrOutputParser()
        response = chain.invoke({"question": question})
    else:
        # Prompt
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI(model_name=constants.LLM_MODEL, temperature=0.3, streaming=True)
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"context": docs, "question": question})
    
    return {"messages": response}