# Movie RAG Orchestrator

## Deploy

[![Build Status](#)]()  
[![Quality Gate Status](#)]()  
[![Coverage](#)]()  
[![Code Smells](#)]()  
[![Duplicated Lines (%)](#)]()  
[![Lines of Code](#)]()

---

#### Introducción

Microservicio encargado de orquestar respuestas generadas por modelos LLM a partir de información sobre películas almacenadas en una base de datos vectorial. Expone un API vía FastAPI, conectado a PostgreSQL con `pgvector` y herramientas de IA generativa como OpenAI, Gemini o modelos LLM locales.

---

### CONTENIDO

* [Requisitos](#requisitos)
* [Para empezar](#para-empezar)
* [Entrypoints](#entrypoints)
* [Variables de entorno](#variables-de-entorno)
* [Swagger](#swagger)
* [Arquitectura y despliegue](#arquitectura)
* [Licencia](#licencia)

---

<a name="requisitos"></a>

#### Requisitos

* Python 3.12
* Docker y Docker Compose
* PostgreSQL + pgvector
* OpenAI API key o Gemini API key
* Make (opcional)

---

<a name="para-empezar"></a>

#### Para empezar

1. Clona el proyecto y accede a la raíz del repositorio.
2. Crea un entorno virtual:

```bash
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Configura tus variables en el archivo `.env` basado en `config.env`.

<a name="entrypoints"></a>

### Entrypoints

| Método | Endpoint | Descripción                                 |
|--------|----------|---------------------------------------------|
| POST   | `/ask`   | Recibe una pregunta y devuelve respuesta de LLM |

---

<a name="variables-de-entorno"></a>

### Variables de entorno

| Variable          | Descripción                                                   |
|-------------------|---------------------------------------------------------------|
| `OPENAI_API_KEY`  | API key de OpenAI                                             |
| `GEMINI_API_KEY`  | API key de Gemini                                             |
| `PG_HOST`         | Host de PostgreSQL                                            |
| `PG_PORT`         | Puerto del motor                                              |
| `PG_USER`         | Usuario de la base de datos                                   |
| `PG_PASSWORD`     | Contraseña del usuario                                        |
| `PG_DATABASE`     | Nombre de la base de datos                                    |
| `EMBEDDING_MODE`  | `local` o `openai`                                            |
| `LLM_PROVIDER`    | `openai`, `gemini`, `local                                    |
| `SQL_FILES`       | Lista de archivos SQL para crear y poblar la DB               |
| `TIMEOUT`         | Tiempo máximo de respuesta en milisegundos                    |
| `SIMILARITY_THRESHOLD` | Umbral mínimo de similitud (entre 0 y 1) para considerar que un documento es relevante. Por defecto es 0.40. Si ninguna coincidencia supera este valor, se devolverá un mensaje indicando que no hubo resultados claros.                       |

<a name="swagger"></a>

### Swagger

Puedes acceder a la documentación interactiva de la API en: http://localhost:8000/docs

<a name="arquitectura"></a>

### Arquitectura y despliegue

Este proyecto puede desplegarse en AWS siguiendo la arquitectura de referencia:

- **EC2**: instancia que ejecuta la API desarrollada en FastAPI.
- **ALB (Application Load Balancer)**: expone la API de forma interna o pública.
- **RDS PostgreSQL con pgvector**: base de datos optimizada para almacenamiento y búsqueda de vectores (embeddings).
- **Llamadas a LLM externo**: integración con proveedores como **OpenAI** o **Gemini** para procesamiento de lenguaje natural.

Puedes visualizar el diagrama de arquitectura en el archivo: docs/aws_architecture.png

