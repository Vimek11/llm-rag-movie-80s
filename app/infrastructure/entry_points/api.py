from fastapi import APIRouter, HTTPException
from app.domain.model.movies.request.query import Question
from app.domain.model.movies.response.answer import Answer 
from app.domain.usecase.rag_usecase import run_rag
from app.infrastructure.driven_adapters.llm_provider import get_llm_provider
from app.infrastructure.driven_adapters.vector_store.postgres_vector_store import PostgresVectorStore
from app.infrastructure.driven_adapters.prompt_provider.yaml_prompt_provider import YamlPromptProvider  # ✅ nuevo

router = APIRouter()

@router.post("/ask")
def ask_question(payload: Question):
    llm = get_llm_provider()
    vector_store = PostgresVectorStore()
    prompt_provider = YamlPromptProvider()

    try:
        response = run_rag(
            question=payload.question,
            top_k=payload.top_k,
            llm=llm,
            vector_store=vector_store,
            prompt_provider=prompt_provider
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
