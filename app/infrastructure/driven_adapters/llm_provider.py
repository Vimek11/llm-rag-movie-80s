import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from app.domain.model.llm.llm_provider import LLMProvider
from .llm.gemini_provider import GeminiProvider
from .llm.openai_provider import OpenAIProvider
from .llm.local_provider import LocalProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv("config.env")

def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "").lower()
    logger.info("Selecting LLM provider: %s", provider)

    if provider == "gemini":
        logger.info("Using Gemini provider.")
        return GeminiProvider()
    elif provider == "openai":
        logger.info("Using OpenAI provider.")
        return OpenAIProvider()
    elif provider == "local":
        logger.info("Using Local provider.")
        return LocalProvider()
    else:
        logger.error("Invalid LLM_PROVIDER: %s", provider)
        raise ValueError(f"LLM_PROVIDER '{provider}' is not valid.")
