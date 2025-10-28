from langchain_core.prompts import ChatPromptTemplate

from app.utils.llm_config import get_openai_llm

llm = get_openai_llm()

prompt = ChatPromptTemplate.from_template(
    """
    For the following careers:
    {careers}

    Suggest one free leaning platform or online corse per career.
    Format: Career - Platform: Cource Title - URL
    Be concise and helpful.
    """
    
)

def get_resource_chain():
    return prompt | llm

