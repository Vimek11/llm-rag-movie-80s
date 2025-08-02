import os
import time
import logging
import pandas as pd
import psycopg2
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv
from openai import OpenAI
import httpx
from sentence_transformers import SentenceTransformer

load_dotenv("config.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MODE = os.getenv("EMBEDDING_MODE", "local")
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY, http_client=httpx.Client(verify=False))
local_model = SentenceTransformer("all-MiniLM-L6-v2")

PG_CONFIG = {
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "dbname": os.getenv("PG_DATABASE")
}

TABLE_NAME = "movies" if MODE == "openai" else "movies_local"

logger.info(f"Modo de embedding: {MODE.upper()} - Tabla destino: {TABLE_NAME}")

def validate_csv(path):
    logger.info(f"Validando archivo: {path}")
    df = pd.read_csv(path)

    required_columns = {"title", "image", "plot"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"El CSV debe tener las columnas: {required_columns}")

    df = df.dropna(subset=["title", "plot"])
    df["title"] = df["title"].astype(str).str.strip()
    df["plot"] = df["plot"].astype(str).str.strip()
    df = df.reset_index(drop=True)

    logger.info(f"Total de películas válidas: {len(df)}")
    return df

def generate_embedding(text):
    try:
        if MODE == "openai":
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        else:
            return local_model.encode(text).tolist()
    except Exception as e:
        logger.error(f"Error generando embedding: {e}")
        return None

def index_to_pgvector(df):
    logger.info(f"Conectando a base de datos: {PG_CONFIG['dbname']}...")

    try:
        conn = psycopg2.connect(**PG_CONFIG)
        logger.info("Conexión a PostgreSQL exitosa.")
    except Exception as e:
        logger.error(f"Error conectando a PostgreSQL: {e}")
        return

    register_vector(conn)
    cursor = conn.cursor()

    for i, row in df.iterrows():
        title, image, plot = row["title"], row["image"], row["plot"]
        
        embedding_plot = generate_embedding(plot)
        embedding_title = generate_embedding(title)

        if embedding_plot is None or embedding_title is None:
            logger.warning(f"Embedding fallido para: {title}")
            continue

        try:
            cursor.execute(f"""
                INSERT INTO {TABLE_NAME} (title, image, plot, embedding_plot, embedding_title)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, image, plot, embedding_plot, embedding_title))

            if (i + 1) % 5 == 0:
                logger.info(f"{i + 1} películas insertadas")
                conn.commit()

        except Exception as e:
            logger.error(f"Error insertando '{title}': {e}")

        if MODE == "openai":
            time.sleep(1.1)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Indexado completo. Conexión cerrada.")


if __name__ == "__main__":
    dataset_path = "../data/movies-dataset.csv"
    df = validate_csv(dataset_path)
    index_to_pgvector(df)
