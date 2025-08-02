from pydantic import BaseModel
from typing import List

class DocumentResponse(BaseModel):
    title: str
    image: str
    similarity: float
    content: str

class RAGResponse(BaseModel):
    results: List[DocumentResponse]
    answer: str
