import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.driven_adapters.vector_store.postgres_vector_store import PostgresVectorStore

@patch("app.infrastructure.driven_adapters.vector_store.postgres_vector_store.psycopg2.connect")
def test_get_similar_documents_success(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("Matrix", "matrix.jpg", "Neo discovers the truth", 0.95),
        ("Inception", "inception.jpg", "Dreams within dreams", 0.93),
    ]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    store = PostgresVectorStore()
    results = store.get_similar_documents([0.1] * 384, top_k=2)

    assert len(results) == 2
    assert results[0]["title"] == "Matrix"
    assert results[1]["similarity"] == 0.93

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("app.infrastructure.driven_adapters.vector_store.postgres_vector_store.psycopg2.connect", side_effect=Exception("Connection failed"))
def test_get_similar_documents_error(mock_connect):
    store = PostgresVectorStore()
    results = store.get_similar_documents([0.2] * 384)
    assert results == []
