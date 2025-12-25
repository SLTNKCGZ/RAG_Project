from typing import Dict, List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.retrieval.retriever import Retriever

class KeywordRetriever(Retriever):

    def __init__(self, top_k: int):
        self.__top_k = top_k

    def __safe_lower(self, s: str) -> str:
        return s.lower() if s is not None else ""

    def __count_occurrences(self, haystack_lower: str, needle_lower: str) -> int:
        if not haystack_lower or not needle_lower:
            return 0
        return haystack_lower.count(needle_lower)

    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
        if not query_terms:
            return []

        hit_map: Dict[str, Hit] = {}

        for chunk in store.get_all_chunks():
            chunk_text_lower = self.__safe_lower(chunk.get_text())
            total_tf = 0

            for term in query_terms:
                if not term:
                    continue
                total_tf += self.__count_occurrences(chunk_text_lower, term.lower())

            if total_tf <= 0:
                continue

            key = f"{chunk.get_doc_id()}||{chunk.get_chunk_id()}"
            hit = hit_map.get(key)

            if hit is None:
                hit = Hit(chunk.get_doc_id(), chunk.get_chunk_id(), total_tf)
                hit_map[key] = hit
            else:
                hit.set_score(hit.get_score() + total_tf)

        hits: List[Hit] = list(hit_map.values())

        hits.sort(key=lambda h: (
            -h.get_score(),           
            h.get_doc_id(),           
            h.get_chunk_id()
        ))
        
        return hits[:self.__top_k]
