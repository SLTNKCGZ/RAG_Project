from typing import Dict, List, Optional
import re

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit
from src.retrieval.retriever import Retriever
from src.writer.simple_stemmer import SimpleStemmer


class KeywordRetriever(Retriever):

    def __init__(self, top_k: int, stemmer: Optional[SimpleStemmer] = None):
        self.__top_k = top_k
        self.__stemmer = stemmer

    def __safe_lower(self, s: str) -> str:
        return s.lower() if s is not None else ""

    def __extract_words(self, text: str) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        if self.__stemmer:
            return [self.__stemmer.stem(word) for word in words]
        return words

    def __count_term_matches(self, chunk_words: List[str], query_term: str) -> int:
        if not chunk_words or not query_term:
            return 0
        
        query_term_lower = query_term.lower()
        query_stem = self.__stemmer.stem(query_term_lower) if self.__stemmer else query_term_lower
        
        return chunk_words.count(query_stem)

    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
        if not query_terms:
            return []

        hit_map: Dict[str, Hit] = {}

        for chunk in store.get_all_chunks():
            chunk_text = self.__safe_lower(chunk.get_text())
            chunk_words = self.__extract_words(chunk_text)
            
            total_tf = 0

            for term in query_terms:
                if not term:
                    continue
                total_tf += self.__count_term_matches(chunk_words, term)

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
