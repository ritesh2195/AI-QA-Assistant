from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from config import GROQ_API_KEY, GROQ_MODEL,OPENAI_MODEL, OPENAI_API_KEY

def get_llm_model(model="groq"):
    if model == "groq":
        return ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY)
    elif model == "openai":
        return ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY)