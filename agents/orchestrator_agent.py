import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from agents.create_automation_code_agent import create_automation_code_agent
from agents.create_test_case_agent import create_test_case_agent
from agents.fetch_story_requirement_agent import fetch_story_requirement_agent
from models.QAState import QAState
from config import GROQ_API_KEY, GROQ_MODEL

# -------------------------
# Schema & Parser
# -------------------------
schemas = [
    ResponseSchema(name="decision", description="Either 'accept' or 'rework'", type="string"),
    ResponseSchema(name="reason", description="Reason for rework, or 'N/A' if accepted", type="string"),
]

schema_parser = StructuredOutputParser.from_response_schemas(schemas)

# -------------------------
# Review Chain
# -------------------------
prompt_review = ChatPromptTemplate.from_messages([
    ("system", """
    You are a QA lead reviewing test cases and automation code.

    Your task:
    1. Decide if the requirement/test case/code is acceptable overall.
    2. If acceptable, return only one JSON object:
        {{ "decision": "accept", "reason": "N/A" }}
    3. If not acceptable, return only one JSON object:
        {{ "decision": "rework", "reason": "<overall feedback>" }}

    Return ONLY valid JSON in this format. Do not include lists, notes, or explanations.
    Review this input:
    {output}
    """),
    ("human", "Review the following:\n{output}\n{format_instructions}")
    ]).partial(format_instructions=schema_parser.get_format_instructions())

review_llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
review_chain = prompt_review | review_llm | schema_parser


# -------------------------
# Retry Helper (feedback loop)
# -------------------------
def run_with_feedback(agent_func, state: QAState, attr: str, step_name: str, max_retries: int):

    for attempt in range(max_retries):
        # Run agent, pass feedback if not first attempt
        feedback = state.reviews[-1]["reason"] if attempt > 0 else None
        state = agent_func(state, feedback=feedback)

        # Get the output to review
        output = getattr(state, attr)

        # Ask reviewer
        review = review_chain.invoke({"output": output})
        state.reviews.append({"step": step_name, "attempt": attempt + 1, **review})

        if review["decision"].lower() == "accept":
            return state

    return state


# -------------------------
# Orchestrator Agent
# -------------------------
def orchestrator_agent(state: QAState, max_retries: int = 3):
    print("🔹 Extracting Requirement...")
    state = run_with_feedback(fetch_story_requirement_agent, state, "requirement", "Requirement Extraction", max_retries)
    if not state.reviews or state.reviews[-1]["decision"].lower() != "accept":
        return state

    print("🔹 Creating Manual Test Cases...")
    state = run_with_feedback(create_test_case_agent, state, "test_case", "Test Case Generation", max_retries)
    if not state.reviews or state.reviews[-1]["decision"].lower() != "accept":
        return state

    print("🔹 Creating Automation Code...")
    state = run_with_feedback(create_automation_code_agent, state, "automation_code", "Automation Code Generation", max_retries)
    if not state.reviews or state.reviews[-1]["decision"].lower() != "accept":
        return state

    print("✅ Orchestration Complete.")
    return state
