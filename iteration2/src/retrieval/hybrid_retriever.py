from typing import List, Dict

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.retrieval.retriever import Retriever


class HybridRetriever(Retriever):
    """
    Late-fusion retriever that combines keyword and vector scores.
    """

    def __init__(
        self,
        keyword_retriever: Retriever,
        vector_retriever: Retriever,
        alpha: float,
        beta: float,
        top_k: int
    ):
        self.__keyword_retriever = keyword_retriever
        self.__vector_retriever = vector_retriever
        self.__alpha = alpha
        self.__beta = beta
        self.__top_k = top_k

    def retrieve(
        self,
        query_terms: List[str],
        store: ChunkStore
    ) -> List[Hit]:
        keyword_hits = self.__keyword_retriever.retrieve(query_terms, store)
        vector_hits = self.__vector_retriever.retrieve(query_terms, store)

        merged: Dict[str, float] = {}

        # keyword scores
        for hit in keyword_hits:
            key = f"{hit.get_doc_id()}||{hit.get_chunk_id()}"
            merged[key] = merged.get(key, 0.0) + self.__alpha * hit.get_score()

        # vector scores
        for hit in vector_hits:
            key = f"{hit.get_doc_id()}||{hit.get_chunk_id()}"
            merged[key] = merged.get(key, 0.0) + self.__beta * hit.get_score()

        hits: List[Hit] = []

        for key, score in merged.items():
            doc_id, chunk_id = key.split("||")
            hits.append(
                Hit(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    score=int(score)
                )
            )

        hits.sort(key=lambda h: (
            -h.get_score(),
            h.get_doc_id(),
            h.get_chunk_id()
        ))

        return hits[:self.__top_k]