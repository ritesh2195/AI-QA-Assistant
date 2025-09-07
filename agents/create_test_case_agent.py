from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from models.QAState import QAState
from config import GROQ_API_KEY, GROQ_MODEL

def create_test_case_agent(state:QAState, feedback: str = None):
    response_schemas = [
        ResponseSchema(name="Title", description="requirement of test case", type="str"),
        ResponseSchema(name="steps", description="A list of ordered test steps", type="list"),
        ResponseSchema(name="expectedResult", description="Expected outcome of the test", type="string"),
    ]
    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    template_text = (
        "You are a QA engineer. Write all the possible clear manual test case including positive, negative and edge case scenarios. Write better title."
        " Requirement: {requirement}\n\nReturn ONLY valid JSON. Do not include explanations, notes, or extra text. The response must strictly follow this format:\n{format_instructions}"
    )

    if feedback:
        template_text += f"\nConsider this reviewer feedback when improving the requirement:\n{feedback}\n"

    prompt_tc = ChatPromptTemplate.from_messages([
        ("system", template_text),
        ("human", "{requirement}\n\nReturn ONLY valid JSON. Do not include explanations, notes, or extra text. The response must strictly follow this format:\n{format_instructions}")
    ])

    if feedback:
        prompt_tc += f"\nConsider this reviewer feedback when improving the requirement:\n{feedback}\n"

    llm_tc = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)

    chain_tc = prompt_tc | llm_tc
    response =  chain_tc.invoke({"requirement":state.requirement, "format_instructions": parser.get_format_instructions()})

    state.test_case = response.content

    return state