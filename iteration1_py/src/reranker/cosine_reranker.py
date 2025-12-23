from typing import List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.reranker.reranker import Reranker


class CosineReranker(Reranker):
    """
    Stub class for a cosine-similarity-based reranking strategy.

    """

    def __init__(self) -> None:
        # Add any dependencies (e.g., embedding provider) via constructor later.
        pass

    def rerank(self, query: List[str], hits: List[Hit], store: ChunkStore) -> List[Hit]:
        # TODO: Implement cosine-similarity-based reranking.
        # For now this is intentionally left empty as a stub.
        return hits


