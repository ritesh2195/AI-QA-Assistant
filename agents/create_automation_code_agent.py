from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from models.QAState import QAState

prompt_aa = ChatPromptTemplate.from_messages(
    [
        ("system","""You are an expert QA Automation engineer expertise in Playwright with c# using NUnit.
         write automation code based on the {test_case}.
          don't include any explanation or notes and don't use BDD """),
        ("human","{test_case}")
    ]
)

llm_aa = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY)

chain_aa = prompt_aa|llm_aa

def create_automation_code_agent(state:QAState):
    response_aa = chain_aa.invoke({"test_case":state.test_case})
    state.automation_code = response_aa.content
    return state