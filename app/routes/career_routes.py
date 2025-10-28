from fastapi import APIRouter
from pydantic import BaseModel
import openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/career")
async def get_career_suggestions(data: PromptRequest):
    prompt = data.prompt

    # --- You can replace this with your agent or chain later ---
    # For now, let's use a simple structured OpenAI response:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a career advisor. Return JSON with career title, skills, salary, and resources."},
            {"role": "user", "content": f"Suggest 3 careers for: {prompt}."}
        ],
        temperature=0.8,
    )

    text = response.choices[0].message["content"]

    # For safety, simulate parsed data (you can JSON.parse actual model output later)
    careers = [
        {"title": "Software Engineer", "skills": ["Python", "APIs"], "salary": "₹8–15 LPA", "resources": ["https://roadmap.sh/backend"]},
        {"title": "AI Developer", "skills": ["ML", "Python"], "salary": "₹10–18 LPA", "resources": ["https://www.kaggle.com"]},
    ]

    return {"careers": careers}
