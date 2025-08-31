from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from models.QAState import QAState

prompt_rq = PromptTemplate(
    input_variables=['description'],
    template='You are a QA Analyst. Extract clear, testable requirements based on the jira {description}'
)

llm_rq = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY)
chain_rq = prompt_rq | llm_rq

def fetch_story_requirement_agent(state: QAState):
    response = chain_rq.invoke({"description": state.description})
    state.requirement = response.content

    return state