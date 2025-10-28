from langchain_core.prompts import ChatPromptTemplate

from app.utils.llm_config import get_openai_llm

llm = get_openai_llm()

prompt = ChatPromptTemplate.from_template(
    """
    A Student is interested in: {interests}
    Suggest 3 career options based on this. Keep responses short and numbered.
    """
)

def get_interest_chain():
    return prompt | llm

