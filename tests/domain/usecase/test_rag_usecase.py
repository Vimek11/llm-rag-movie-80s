import pytest
from unittest.mock import MagicMock
from app.domain.usecase.rag_usecase import run_rag

def test_run_rag_success():
    mock_llm = MagicMock()
    mock_vector_store = MagicMock()
    mock_llm.extract_topic.return_value = "science fiction"
    mock_llm.ask.return_value = "You should watch Interstellar."
    mock_vector_store.get_similar_documents.return_value = [
        {
            "title": "Interstellar",
            "image": "interstellar.jpg",
            "content": "A team of explorers travel through a wormhole...",
            "similarity": 0.95
        }
    ]

    question = "What movie should I watch if I like space adventures?"
    top_k = 1

    result = run_rag(question, top_k, mock_llm, mock_vector_store)

    assert isinstance(result, dict)
    assert "answer" in result
    assert "results" in result
    assert result["answer"] == "You should watch Interstellar."
    assert len(result["results"]) == 1

    mock_llm.extract_topic.assert_called_once_with(question)
    mock_vector_store.get_similar_documents.assert_called_once()
    mock_llm.ask.assert_called_once()
