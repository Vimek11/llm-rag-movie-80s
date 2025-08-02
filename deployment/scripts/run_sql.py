import os
import psycopg2
import logging
from dotenv import load_dotenv

load_dotenv("config.env")

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

SQL_FILES = os.getenv("SQL_FILES", "create_tables.sql").split(',')  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_sql_file(file_path):
    try:
        with open(os.path.join('sql', file_path), 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error("Archivo SQL no encontrado: %s", file_path)
        raise

def setup_db():
    try:
        logger.info(f"Conectando a PostgreSQL en {PG_HOST}:{PG_PORT}...")
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            dbname=PG_DATABASE
        )
        conn.autocommit = True
        cursor = conn.cursor()

        for sql_file in SQL_FILES:
            logger.info(f"Ejecutando el script SQL: {sql_file}")
            sql = read_sql_file(sql_file.strip()) 
            cursor.execute(sql)
            logger.info(f"Script {sql_file} ejecutado exitosamente.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error("Error al ejecutar los scripts SQL: %s", e)

if __name__ == "__main__":
    setup_db()
