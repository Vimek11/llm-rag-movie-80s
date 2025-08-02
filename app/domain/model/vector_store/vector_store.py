from abc import ABC, abstractmethod
from typing import List

class VectorStore(ABC):
    @abstractmethod
    def get_similar_documents(self, embedding: list[float], top_k: int = 3) -> List[dict]:
        pass
