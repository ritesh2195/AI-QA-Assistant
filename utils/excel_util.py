import pandas as pd
import os

# Path of the folder you want to create
test_case_folder_path = "TestCases"
os.makedirs(test_case_folder_path, exist_ok=True)
test_case_path = os.path.join(test_case_folder_path,"test_case.xlsx")

def write_test_cases_to_excel(test_cases, filepath=test_case_path):
    """
    Writes the generated test cases into an Excel file.
    Each test case may have multiple steps.
    """
    rows = []
    for tc in test_cases:
        steps = tc.get("steps", [])
        for i, step in enumerate(steps):
            row = {
                "Title": tc.get("Title") if i == 0 else "",
                "Step": step,
                "Expected Result": tc.get("expectedResult") if i == len(steps) - 1 else ""
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(filepath, index=False)
    print(f"✅ Test cases written to {filepath}")
