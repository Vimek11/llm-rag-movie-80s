import os
import pytest
from app.infrastructure.driven_adapters.llm_provider import get_llm_provider
from app.infrastructure.driven_adapters.llm.gemini_provider import GeminiProvider
from app.infrastructure.driven_adapters.llm.openai_provider import OpenAIProvider
from app.infrastructure.driven_adapters.llm.local_provider import LocalProvider

@pytest.mark.parametrize("provider_name,expected_class", [
    ("gemini", GeminiProvider),
    ("openai", OpenAIProvider),
    ("local", LocalProvider),
])
def test_get_llm_provider_valid(monkeypatch, provider_name, expected_class):
    monkeypatch.setenv("LLM_PROVIDER", provider_name)
    provider_instance = get_llm_provider()
    assert isinstance(provider_instance, expected_class)

def test_get_llm_provider_invalid(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "invalid_provider")
    with pytest.raises(ValueError, match="LLM_PROVIDER 'invalid_provider' is not valid."):
        get_llm_provider()
