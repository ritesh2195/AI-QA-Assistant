from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from models.QAState import QAState

def fetch_story_requirement_agent(state: QAState, feedback: str = None):
    template = (
        "You are a QA Analyst. Extract clear, testable requirements based on the jira {description}."
    )
    if feedback:
        template += f" Consider this reviewer feedback when improving the requirement: {feedback}"

    prompt_rq = PromptTemplate(
        input_variables=['description'],
        template=template
    )

    llm_rq = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    chain_rq = prompt_rq | llm_rq
    response = chain_rq.invoke({"description": state.description})
    state.requirement = response.content

    return state