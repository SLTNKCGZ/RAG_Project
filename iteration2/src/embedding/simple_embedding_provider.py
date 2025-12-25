from typing import List
from src.embedding.embedding_provider import EmbeddingProvider

class SimpleEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic stub embedding provider.
    Same text -> same vector always.
    """

    def embed(self, text: str) -> List[float]:
        vector = [0.0] * 8
        if not text:
            return vector

        for i, ch in enumerate(text.lower()):
            vector[i % 8] += (ord(ch) % 10)

        return vector