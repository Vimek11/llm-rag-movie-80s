import os
import logging
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from app.domain.model.llm.llm_provider import LLMProvider
from app.domain.model.vector_store.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
model = SentenceTransformer("all-MiniLM-L6-v2")

def run_rag(question: str, top_k: int, llm: LLMProvider, vector_store: VectorStore) -> dict:
    title = llm.extract_title(question)
    print("Extracted title:", title)

    documents = []

    if title.lower() != "false":
        title_embedding = model.encode(title).tolist()
        documents = vector_store.get_similar_documents(title_embedding, top_k, field="title")

    if not documents:
        topic = llm.extract_topic(question)
        print("Extracted topic:", topic)
        topic_embedding = model.encode(topic).tolist()
        documents = vector_store.get_similar_documents(topic_embedding, top_k, field="plot")

    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD"))
    high_similarity_docs = [doc for doc in documents if doc["similarity"] >= SIMILARITY_THRESHOLD]

    if not high_similarity_docs:
        return {
            "answer": "No se encontraron coincidencias claras con películas de los años 80. Intenta reformular tu pregunta para obtener mejores resultados.",
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

    prompt = f"""
        Use the following movie information to answer the user's question. If any movie clearly matches the question, mention its title.
        Information:
        {context}
        Original question:
        {question}
    """.strip()

    answer = llm.ask(prompt)
    return {"answer": answer, "results": high_similarity_docs}
