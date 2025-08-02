from app.domain.model.llm.llm_provider import LLMProvider

class LocalProvider(LLMProvider):
    def ask(self, prompt: str) -> str:
        return "[LOCAL] Not implemented yet"

    def extract_topic(self, question: str) -> str:
        return "[LOCAL] Not implemented yet"
