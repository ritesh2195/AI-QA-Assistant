"""
Centralized configuration. Values are loaded from environment variables when present,
with safe defaults for local/dev runs. Use a .env file for local overrides.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

# Jira
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", os.getenv('JIRA_BASE_URL'))
JIRA_EMAIL = os.getenv("JIRA_EMAIL", os.getenv('JIRA_EMAIL'))
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", os.getenv('JIRA_API_TOKEN'))
# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", os.getenv('OPENAI_API_KEY'))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change if needed

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", os.getenv('OPENAI_API_KEY'))
GROQ_MODEL = os.getenv("GROQ_MODEL", "Gemma2-9b-It")  # change if needed