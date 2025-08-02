import os
import psycopg2
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MODE = os.getenv("EMBEDDING_MODE", "local")
TABLE_NAME = "movies" if MODE == "openai" else "movies_local"

def get_similar_documents(embedding, top_k=3, field="plot"):
    logger.info("Connecting to the database...")

    # Validación de campo
    embedding_column = {
        "plot": "embedding_plot",
        "title": "embedding_title"
    }.get(field)

    if embedding_column is None:
        logger.error(f"Invalid field: '{field}'. Must be 'plot' or 'title'.")
        return []

    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            dbname=os.getenv("PG_DATABASE"),
        )
        cur = conn.cursor()
        logger.info("Database connection established.")

        query = f"""
            SELECT title, image, plot, 1 - ({embedding_column} <=> %s::vector) AS similarity
            FROM {TABLE_NAME}
            ORDER BY {embedding_column} <=> %s::vector
            LIMIT %s;
        """

        logger.info(f"Executing query using field '{embedding_column}'...")
        cur.execute(query, (embedding, embedding, top_k))
        results = cur.fetchall()
        logger.info("Query executed successfully. Retrieved %d results.", len(results))

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
        logger.exception("An error occurred while retrieving similar documents.")
        return []
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
            logger.info("Database connection closed.")
