from fastapi import APIRouter
from app.domain.model.movies.request.query import Question
from app.domain.model.movies.response.answer import Answer 
from app.domain.usecase.rag_usecase import run_rag
from app.infrastructure.driven_adapters.llm_provider import get_llm_provider
from app.infrastructure.driven_adapters.vector_store.postgres_vector_store import PostgresVectorStore

router = APIRouter()
llm = get_llm_provider()

@router.post("/ask")
def ask_question(payload: Question):
    llm = get_llm_provider()
    vector_store = PostgresVectorStore() 
    try:
        response = run_rag(payload.question, payload.top_k, llm, vector_store)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
