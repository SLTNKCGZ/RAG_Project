from typing import List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.reranker.reranker import Reranker


class HybridReranker(Reranker):
    """
    Final decision reranker.
    Does NOT recompute scores.
    Only orders incoming hits deterministically.
    """

    def __init__(self, alpha: float, beta: float):
        # alpha, beta kept for configurability / future use
        self.__alpha = alpha
        self.__beta = beta

    def rerank(
        self,
        query: List[str],
        hits: List[Hit],
        store: ChunkStore
    ) -> List[Hit]:
        if not hits:
            return []

        # IMPORTANT:
        # Do NOT modify scores here.
        reranked = list(hits)

        reranked.sort(
            key=lambda h: (
                -h.get_score(),
                h.get_doc_id(),
                h.get_chunk_id()
            )
        )

        return reranked