import json
import logging
import os
from typing import List, Union

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field, ValidationError, field_validator

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

# Model for /career; override with OPENAI_MODEL in the environment.
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are a career advisor for students in India. "
    "Reply with a JSON object only, in exactly this shape: "
    '{"careers": [{"title": string, "skills": [string, ...], '
    '"salary": string, "resources": [string, ...]}]}. '
    "Return exactly 3 careers. For each: 'skills' lists the top 3 skills, "
    "'salary' is the expected annual salary range in INR (for example \"₹6–12 LPA\"), "
    "and 'resources' lists 1–2 URLs of free learning resources."
)


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class Career(BaseModel):
    title: str
    skills: List[str] = []
    salary: str = ""
    resources: List[str] = []

    @field_validator("skills", "resources", mode="before")
    @classmethod
    def _to_list(cls, value: Union[str, list, None]):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return [str(item) for item in value]


class CareerResponse(BaseModel):
    careers: List[Career]


_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured on the server")
        _client = OpenAI()  # reads OPENAI_API_KEY from the environment
    return _client


def _parse_careers(text: str) -> CareerResponse:
    data = json.loads(text)
    if isinstance(data, list):  # tolerate a bare list of careers
        data = {"careers": data}
    return CareerResponse.model_validate(data)


@router.post("/career", response_model=CareerResponse)
def get_career_suggestions(data: PromptRequest):
    client = _get_client()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Suggest 3 careers for: {data.prompt}"},
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
        )
    except OpenAIError as exc:
        logger.exception("OpenAI request failed")
        raise HTTPException(status_code=502, detail=f"AI service error: {exc.__class__.__name__}") from exc

    text = completion.choices[0].message.content or ""
    try:
        result = _parse_careers(text)
    except (json.JSONDecodeError, ValidationError) as exc:
        logger.warning("Could not parse model output: %r", text[:500])
        raise HTTPException(status_code=502, detail="Could not parse the AI response") from exc

    if not result.careers:
        raise HTTPException(status_code=502, detail="The AI response contained no careers")

    return result
