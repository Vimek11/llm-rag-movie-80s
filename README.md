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
* [Pruebas y cobertura](#Pruebas-y-cobertura)
* [Pruebas de aceptación](#Prueba-de-aceptación)

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


<a name="Pruebas-y-cobertura"></a>

## Pruebas y cobertura

Este proyecto utiliza `pytest` junto con `pytest-cov` para asegurar la calidad del código y medir la cobertura de pruebas.

###  Ejecutar pruebas con cobertura

Asegúrate de tener instaladas las dependencias:

```bash
pip install -r requirements.txt

pytest --cov=app tests/

```

<a name="#Prueba-de-aceptación"></a>

### Pruebas de aceptación 

Las pruebas de aceptación están escritas en formato Gherkin y ejecutadas con `behave`.

#### 1. Asegúrate de que la API esté corriendo

Inicia el servidor local en otra terminal:

```bash
uvicorn app.infrastructure.entry_points.api:app --reload
```
#### 2. Asegúrate de que la API esté corriendo

Ejecuta en otra terminal dentro de acceptance-test:

```bash
behave
```