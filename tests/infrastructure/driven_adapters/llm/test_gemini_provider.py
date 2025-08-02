import pytest
from unittest.mock import MagicMock, patch
from app.infrastructure.driven_adapters.llm.gemini_provider import GeminiProvider

def test_ask_success():
    provider = GeminiProvider()
    mock_response = MagicMock()
    mock_response.text = " This is a Gemini response. "

    with patch("app.infrastructure.driven_adapters.llm.gemini_provider.model.generate_content", return_value=mock_response):
        response = provider.ask("Hello Gemini")
        assert response == "This is a Gemini response."

def test_ask_failure():
    provider = GeminiProvider()

    with patch("app.infrastructure.driven_adapters.llm.gemini_provider.model.generate_content", side_effect=Exception("Gemini error")):
        response = provider.ask("Hello Gemini")
        assert response == ""

def test_extract_topic():
    provider = GeminiProvider()

    with patch.object(provider, "ask", return_value="science fiction"):
        topic = provider.extract_topic("What movie is about AI?")
        assert topic == "science fiction"
