import requests

from config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN


def fetch_jira_issue_tool(issue_key:str):
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}"
    r = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), timeout=30)
    r.raise_for_status()
    response = r.json()

    return response['fields']['description']
