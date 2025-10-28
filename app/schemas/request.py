from pydantic import BaseModel


class CareerQuery(BaseModel):
    interests: str