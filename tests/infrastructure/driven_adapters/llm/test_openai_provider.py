import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.driven_adapters.llm.openai_provider import OpenAIProvider

def test_ask_returns_response():
    provider = OpenAIProvider()
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="  This is a mock answer.  "))]

    with patch("app.infrastructure.driven_adapters.llm.openai_provider.client.chat.completions.create", return_value=mock_response):
        result = provider.ask("Tell me a joke.")
        assert result == "This is a mock answer."

def test_ask_handles_exception():
    provider = OpenAIProvider()

    with patch("app.infrastructure.driven_adapters.llm.openai_provider.client.chat.completions.create", side_effect=Exception("OpenAI down")):
        result = provider.ask("Hello?")
        assert result == ""

def test_extract_topic_calls_ask():
    provider = OpenAIProvider()

    with patch.object(provider, "ask", return_value="science fiction") as mock_ask:
        topic = provider.extract_topic("What movie is about space travel?")
        assert topic == "science fiction"
        mock_ask.assert_called_once()
