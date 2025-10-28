from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY

def get_openai_llm(model = "gpt-4o"):
    return ChatOpenAI(
        model=model,
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY
    )


