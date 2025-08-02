import pytest
from unittest.mock import MagicMock, ANY
from app.domain.usecase.rag_usecase import run_rag

def test_run_rag_success():
    mock_llm = MagicMock()
    mock_llm.extract_title.return_value = "Interstellar"
    mock_llm.extract_topic.return_value = "space adventures"
    mock_llm.ask.return_value = "You should watch Interstellar."

    mock_vector_store = MagicMock()
    mock_vector_store.get_similar_documents.return_value = [
        {
            "title": "Interstellar",
            "image": "interstellar.jpg",
            "content": "A team of explorers travel through a wormhole...",
            "similarity": 0.95
        }
    ]

    mock_prompt_provider = MagicMock()
    mock_prompt_provider.get_prompt.side_effect = lambda key, **kwargs: (
        f"Prompt: {key}\nContext: {kwargs.get('context')}\nQuestion: {kwargs.get('question')}"
        if key == "answer_prompt" else "No matches found."
    )

    question = "What movie should I watch if I like space adventures?"
    top_k = 1

    result = run_rag(question, top_k, mock_llm, mock_vector_store, mock_prompt_provider)

    assert isinstance(result, dict)
    assert "answer" in result
    assert "results" in result
    assert "Interstellar" in result["answer"]
    assert len(result["results"]) == 1

    mock_llm.extract_title.assert_called_once_with(question)
    mock_llm.ask.assert_called_once()
    mock_vector_store.get_similar_documents.assert_called()
    mock_prompt_provider.get_prompt.assert_any_call("answer_prompt", context=ANY, question=question)
