from db import get_similar_documents
from llm import ask_llm
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv("config.env")

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_search_topic(question: str) -> str:
    prompt = f"""
Extrae el concepto general de esta pregunta para hacer una búsqueda semántica de películas.

Pregunta: {question}

Devuelve solo una frase corta en inglés que represente el tema principal. No expliques nada más.
"""
    topic = ask_llm(prompt)
    return topic.strip()


def rag_pipeline(question: str, top_k: int = 3):
    refined_query = extract_search_topic(question)
    print(f"\n🔍 Tópico extraído para búsqueda:\n{refined_query}")

    question_embedding = model.encode(refined_query).tolist()
    vector_store = PostgresVectorStore()
    documents = vector_store.get_similar_documents(embedding, top_k=3)
    #documents = get_similar_documents(question_embedding, top_k=top_k)

    print("\n📚 Películas similares encontradas:\n")
    for i, doc in enumerate(documents, start=1):
        print(f"{i}. 🎬 Título: {doc['title']}")
        print(f"🖼️ Imagen: {doc['image']}")
        print(f"🧠 Similaridad: {doc['similarity']:.4f}")
        print(f"📄 Sinopsis:\n{doc['content'][:400]}...\n{'-'*60}")

    # Construir el contexto que se le pasa al LLM
    context = ""
    for doc in documents:
        context += f"""
Título: {doc['title']}
Imagen: {doc['image']}
Sinopsis: {doc['content']}
---
"""

    prompt = f"""
Usa la siguiente información de películas para responder la pregunta del usuario. Si alguna coincide claramente con lo que se busca, menciona su título.

Información:
{context}

Pregunta original:
{question}
    """.strip()

    answer = ask_llm(prompt)
    return answer


if __name__ == "__main__":
    print("📥 Pregunta de usuario:")
    question = input("Pregunta: ")

    answer = rag_pipeline(question)

    print("\n💬 Respuesta generada por el LLM:\n")
    print(answer)
