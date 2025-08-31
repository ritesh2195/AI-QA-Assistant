import json

from tools.jira_tool import fetch_jira_issue_tool
from workflows.qa_workflow import build_workflow
from utils.excel_util import write_test_cases_to_excel
from utils.code_util import write_automation_code

import os

# Path of the folder you want to create
test_case_folder_path = "TestCases"
automation_folder_path = "TestCode"

os.makedirs(test_case_folder_path, exist_ok=True)
os.makedirs(automation_folder_path, exist_ok=True)

automation_file_path = os.path.join(automation_folder_path, "automation_test.cs")
test_case_path = os.path.join(test_case_folder_path,"test_case.xlsx")

if __name__ == "__main__":
    graph = build_workflow()

    description = fetch_jira_issue_tool("SCRUM-4")

    response = graph.invoke({"description": description})

    json_str = response['test_case'].strip("```json").strip("```").strip()

    # Step 2: Parse JSON
    test_cases = json.loads(json_str)

    automation_code = response['automation_code'].strip("```csharp").strip("```").strip()

    # Save outputs
    write_test_cases_to_excel(test_cases,test_case_path)
    write_automation_code(automation_code,automation_file_path)
