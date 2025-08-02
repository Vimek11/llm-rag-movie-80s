from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        pass

    @abstractmethod
    def extract_topic(self, question: str) -> str:
        pass
