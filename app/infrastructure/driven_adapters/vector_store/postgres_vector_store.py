import os
import psycopg2
import logging
from dotenv import load_dotenv
from typing import List
from app.domain.model.vector_store.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class PostgresVectorStore(VectorStore):
    def __init__(self):
        self.mode = os.getenv("EMBEDDING_MODE", "local")
        self.table_name = "movies" if self.mode == "openai" else "movies_local"
        self.conn_params = {
            "host": os.getenv("PG_HOST"),
            "port": os.getenv("PG_PORT"),
            "user": os.getenv("PG_USER"),
            "password": os.getenv("PG_PASSWORD"),
            "dbname": os.getenv("PG_DATABASE"),
        }

    def get_similar_documents(self, embedding: List[float], top_k: int = 3, field: str = "plot") -> List[dict]:
        # Mapear campo a columna válida
        embedding_column = {
            "plot": "embedding_plot",
            "title": "embedding_title"
        }.get(field)

        if embedding_column is None:
            logger.error(f"Invalid field for similarity search: {field}")
            return []

        logger.info(f"Connecting to PostgreSQL for vector search in field '{field}'...")
        try:
            conn = psycopg2.connect(**self.conn_params)
            cur = conn.cursor()
            logger.info("Connection established. Executing similarity query...")

            query = f"""
                SELECT title, image, plot, 1 - ({embedding_column} <=> %s::vector) AS similarity
                FROM {self.table_name}
                ORDER BY {embedding_column} <=> %s::vector
                LIMIT %s;
            """
            cur.execute(query, (embedding, embedding, top_k))
            results = cur.fetchall()
            logger.info("Query executed. Retrieved %d results.", len(results))

            return [
                {
                    "title": row[0],
                    "image": row[1],
                    "content": row[2],
                    "similarity": row[3]
                }
                for row in results
            ]
        except Exception as e:
            logger.exception("Error during vector similarity query.")
            return []
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
                logger.info("PostgreSQL connection closed.")
