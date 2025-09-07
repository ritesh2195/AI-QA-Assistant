from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from models.QAState import QAState

def create_automation_code_agent(state:QAState, feedback: str = None):

    template_text = (
        "You are an expert QA Automation engineer with expertise in Playwright using C# and NUnit.\n"
        "Write automation code based on the following manual test case: {test_case}.\n"
        "Do not include any explanation or notes, do not use BDD or SpecFlow. Provide only NUnit + Playwright code."
    )

    if feedback:
        template_text += f"\nConsider this reviewer feedback when improving the code:\n{feedback}\n"

    prompt_aa = ChatPromptTemplate.from_messages([
        ("system", template_text),
        ("human", "{test_case}")
    ])

    llm_aa = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)

    chain_aa = prompt_aa | llm_aa
    response_aa = chain_aa.invoke({"test_case":state.test_case})
    state.automation_code = response_aa.content
    return state