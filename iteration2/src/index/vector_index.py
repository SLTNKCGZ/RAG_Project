from typing import Dict, List
import math

from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.embedding.embedding_provider import EmbeddingProvider


class VectorIndex:
    """
    Stores embeddings for all chunks and provides cosine similarity search.
    """

    def __init__(
        self,
        store: ChunkStore,
        embedding_provider: EmbeddingProvider
    ):
        self.__embedding_provider = embedding_provider
        self.__vectors: Dict[str, List[float]] = {}

        self.__build_index(store)

    def __build_index(self, store: ChunkStore) -> None:
        """
        Pre-compute embeddings for all chunks in the store.
        """
        for chunk in store.get_all_chunks():
            key = self.__make_key(chunk)
            self.__vectors[key] = self.__embedding_provider.embed(
                chunk.get_text()
            )

    def __make_key(self, chunk: Chunk) -> str:
        return f"{chunk.get_doc_id()}||{chunk.get_chunk_id()}"

    def __cosine_similarity(
        self,
        v1: List[float],
        v2: List[float]
    ) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def search(
        self,
        query_text: str,
        top_k: int
    ) -> List[tuple[str, float]]:
        """
        Returns (chunk_key, cosine_score) pairs.
        """
        query_vec = self.__embedding_provider.embed(query_text)

        scored = []

        for key, chunk_vec in self.__vectors.items():
            score = self.__cosine_similarity(query_vec, chunk_vec)
            scored.append((key, score))

        scored.sort(key=lambda x: -x[1])
        return scored[:top_k]