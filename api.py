from typing import List
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import json
from pydantic import BaseModel
from config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN
from tools.jira_tool import fetch_jira_issue_tool
from workflows.qa_workflow import build_workflow
from utils.excel_util import write_test_cases_to_excel
from utils.code_util import write_automation_code

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],   # 👈 allow everything for testing
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

# Folders for outputs
TEST_CASE_FOLDER = "TestCases"
AUTOMATION_FOLDER = "TestCode"

os.makedirs(TEST_CASE_FOLDER, exist_ok=True)
os.makedirs(AUTOMATION_FOLDER, exist_ok=True)

TEST_CASE_PATH = os.path.join(TEST_CASE_FOLDER, "test_case.xlsx")
AUTOMATION_FILE_PATH = os.path.join(AUTOMATION_FOLDER, "automation_test.cs")


@app.post("/generate/")
def generate_test_cases(issue_key: str):
    try:
        graph = build_workflow()
        description = fetch_jira_issue_tool(issue_key)

        response = graph.invoke({"description": description})

        # Clean and parse test_case JSON
        json_str = response['test_case'].strip("```json").strip("```").strip()
        test_cases = json.loads(json_str)

        # Clean automation code
        automation_code = response['automation_code'].strip("```csharp").strip("```").strip()

        # Save files
        write_test_cases_to_excel(test_cases, TEST_CASE_PATH)
        write_automation_code(automation_code, AUTOMATION_FILE_PATH)

        return {
            "message": "Test cases and automation code generated successfully!",
            "test_cases": test_cases,
            "automation_code": automation_code
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/excel/")
async def download_excel():
    if not os.path.exists(TEST_CASE_PATH):
        raise HTTPException(status_code=404, detail="Excel file not found")
    return FileResponse(
        path=TEST_CASE_PATH,
        filename="test_case.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/download/cs/")
def download_cs():
    if os.path.exists(AUTOMATION_FILE_PATH):
        return FileResponse(AUTOMATION_FILE_PATH, media_type="text/plain", filename="automation_test.cs")
    raise HTTPException(status_code=404, detail="C# file not found")

class JiraStory(BaseModel):
    key: str
    summary: str


@app.get("/jira/stories", response_model=List[JiraStory])
async def get_stories():
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    query = {"jql": f"project={"SCRUM"}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=query,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json"}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    issues = data.get("issues", [])

    # Transform Jira issues to your model
    stories = [
        JiraStory(
            key=issue["key"],
            summary=issue["fields"]["summary"]
        )
        for issue in issues
    ]

    return stories
