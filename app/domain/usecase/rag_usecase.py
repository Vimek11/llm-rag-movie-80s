import os
import logging
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from app.domain.model.llm.llm_provider import LLMProvider
from app.domain.model.vector_store.vector_store import VectorStore
from app.domain.model.prompt.prompt_provider import PromptProvider  # ✅ nuevo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

def run_rag(
    question: str,
    top_k: int,
    llm: LLMProvider,
    vector_store: VectorStore,
    prompt_provider: PromptProvider
) -> dict:
    title = llm.extract_title(question)

    documents = []

    if title.lower() != "false":
        title_embedding = model.encode(title).tolist()
        documents = vector_store.get_similar_documents(title_embedding, top_k, field="title")

    if not documents:
        topic = llm.extract_topic(question)
        topic_embedding = model.encode(topic).tolist()
        documents = vector_store.get_similar_documents(topic_embedding, top_k, field="plot")

    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.30"))
    high_similarity_docs = [doc for doc in documents if doc["similarity"] >= SIMILARITY_THRESHOLD]

    if not high_similarity_docs:
        return {
            "answer": prompt_provider.get_prompt("error_prompt"),
            "results": [
                {
                    "title": "Sin coincidencias",
                    "image": "https://media.istockphoto.com/id/1472513555/es/vector/personas-deprimidas-sentadas-en-el-suelo-y-abraz%C3%A1ndose-de-rodillas-concepto-de-salud-mental.jpg?s=612x612&w=0&k=20&c=SEeMu7CJ5g5BxvinVGw30o1XFbrm6YcyTq_Jpn6wbIk=",
                    "content": "No se hallaron resultados relevantes para tu pregunta. Puedes intentar especificar mejor el título o contexto de la película.",
                    "similarity": 0.0
                }
            ]
        }

    context = "".join(
        f"""
        Title: {doc['title']}
        Image: {doc['image']}
        Synopsis: {doc['content']}
        ---
        """
        for doc in high_similarity_docs
    )
    prompt = prompt_provider.get_prompt("answer_prompt", context=context, question=question)
    answer = llm.ask(prompt)
    return {"answer": answer, "results": high_similarity_docs}
