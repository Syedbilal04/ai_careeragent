from langchain_core.runnables import RunnableSequence


from app.chains.interest_chain import get_interest_chain
from app.chains.skill_chain import get_skill_chain
from app.chains.resouce_chian import get_resource_chain


interest_chain = get_interest_chain()
skill_chain = get_skill_chain()
resource_chain = get_resource_chain()

def run_career_agent(interests: str) ->dict:

    career_text= interest_chain.invoke({"interests": interests}).content.strip()
    skill_text = skill_chain.invoke({"careers": career_text}).content.strip()
    resource_text = resource_chain.invoke({"careers": career_text}).content.strip()

    return {
        "careers": career_text,
        "skill_and_salary": skill_text,
        "resources": resource_text
    }
