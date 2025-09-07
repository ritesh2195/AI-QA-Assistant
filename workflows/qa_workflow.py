from langgraph.graph import StateGraph, START, END
from agents.create_automation_code_agent import create_automation_code_agent
from agents.create_test_case_agent import create_test_case_agent
from agents.fetch_story_requirement_agent import fetch_story_requirement_agent
from models.QAState import QAState
from agents.orchestrator_agent import orchestrator_agent

def build_workflow():
    graph = StateGraph(QAState)

    # Instead of chaining raw agents, we use the orchestrator
    graph.add_node("orchestrator", orchestrator_agent)

    graph.add_edge(START, "orchestrator")
    graph.add_edge("orchestrator", END)

    return graph.compile()
