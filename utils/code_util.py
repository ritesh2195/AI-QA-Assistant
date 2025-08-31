import os

automation_folder_path = "TestCode"
os.makedirs(automation_folder_path, exist_ok=True)
automation_file_path = os.path.join(automation_folder_path, "automation_test.cs")

def write_automation_code(code: str, filepath):
    """
    Writes the generated automation code into a file.
    Default is a C# file, but you can adjust extension per language.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Automation code written to {filepath}")
