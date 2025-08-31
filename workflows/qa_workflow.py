from langgraph.graph import StateGraph, START, END
from agents.create_automation_code_agent import create_automation_code_agent
from agents.create_test_case_agent import create_test_case_agent
from agents.fetch_story_requirement_agent import fetch_story_requirement_agent
from models.QAState import QAState
from tools.jira_tool import fetch_jira_issue_tool

def build_workflow():
    graph = StateGraph(QAState)

    graph.add_node('fetch_story_requirement_agent', fetch_story_requirement_agent)
    graph.add_node('create_test_case_agent', create_test_case_agent)
    graph.add_node("create_automation_code_agent", create_automation_code_agent)

    graph.add_edge(START, 'fetch_story_requirement_agent')
    graph.add_edge('fetch_story_requirement_agent', 'create_test_case_agent')
    graph.add_edge('create_test_case_agent', "create_automation_code_agent")
    graph.add_edge("create_automation_code_agent", END)

    return graph.compile()
