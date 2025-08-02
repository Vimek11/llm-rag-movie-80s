from pydantic import BaseModel

class Question(BaseModel):
    question: str
    top_k: int = 3
