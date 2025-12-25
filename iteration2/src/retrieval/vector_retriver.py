from typing import List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.retrieval.retriever import Retriever
from src.index.vector_index import VectorIndex


class VectorRetriever(Retriever):
    """
    Retriever that performs semantic search using VectorIndex.
    """

    def __init__(
        self,
        vector_index: VectorIndex,
        top_k: int
    ):
        self.__vector_index = vector_index
        self.__top_k = top_k

    def retrieve(
        self,
        query_terms: List[str],
        store: ChunkStore
    ) -> List[Hit]:
        if not query_terms:
            return []

        query_text = " ".join(query_terms)

        # VectorIndex returns (key, cosine_score)
        results = self.__vector_index.search(
            query_text=query_text,
            top_k=self.__top_k
        )

        hits: List[Hit] = []

        for key, score in results:
            doc_id, chunk_id = key.split("||")

            # scale cosine score to int for deterministic behavior
            hits.append(
                Hit(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    score=int(score * 1000)
                )
            )

        return hits