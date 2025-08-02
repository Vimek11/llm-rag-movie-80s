import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("EMBEDDING_MODE", "local")
TABLE_NAME = "movies" if MODE == "openai" else "movies_local"

def get_similar_documents(embedding, top_k=3):
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE"),
    )
    cur = conn.cursor()

    query = f"""
        SELECT title, image, plot, 1 - (embedding <=> %s::vector) AS similarity
        FROM {TABLE_NAME}
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """
    cur.execute(query, (embedding, embedding, top_k))
    results = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "title": row[0],
            "image": row[1],
            "content": row[2],  
            "similarity": row[3]
        }
        for row in results
    ]
