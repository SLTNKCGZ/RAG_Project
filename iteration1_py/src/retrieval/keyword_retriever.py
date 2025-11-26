from typing import List, Dict

from data.chunk_store import ChunkStore
from model.chunk import Chunk
from model.hit import Hit
from retriever_abstract import Retriever 

class KeywordRetriever(Retriever):

    def __init__(self, top_k: int):
        self.top_k = top_k

    def _safe_lower(self, s: str) -> str:
        return s.lower() if s is not None else ""

    def _count_occurrences(self, haystack_lower: str, needle_lower: str) -> int:
        if not haystack_lower or not needle_lower:
            return 0
        return haystack_lower.count(needle_lower)

    def retrieve(self, query_terms: List[str], store) -> List: 
        if not query_terms:
            return []

        hit_map: Dict[str, object] = {}

        for chunk in store.get_all_chunks():
            chunk_text_lower = self._safe_lower(chunk.get_text())
            total_tf = 0

            for term in query_terms:
                if not term:
                    continue
                total_tf += self._count_occurrences(chunk_text_lower, term.lower())

            if total_tf > 0:
                key = f"{chunk.get_doc_id()}||{chunk.get_chunk_id()}"
                
                h = hit_map.get(key)
                
                if h is None:
                    h = object(chunk.get_doc_id(), chunk.get_chunk_id(), total_tf) 
                else:
                    h.set_score(h.get_score() + total_tf)

        hits: List[object] = list(hit_map.values())

        hits.sort(key=lambda h: (
            -h.get_score(),           
            h.get_doc_id(),           
            h.get_chunk_id()
        ))
        
        return hits[:self.top_k]