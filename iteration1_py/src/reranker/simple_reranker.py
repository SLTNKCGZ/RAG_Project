from typing import List
import collections 
from src.reranker.reranker_abstract import Reranker
from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk
from src.model.hit import Hit 

class SimpleReranker(Reranker):
    
    def __init__(self, proximity_window: int, proximity_bonus: int, title_boost: int):
        self.__proximity_window = proximity_window 
        self.__proximity_bonus = proximity_bonus
        self.__title_boost = title_boost

    def __any_terms_within_window(self, text: str, terms: List[str], window: int) -> bool:
        positions: List[int] = []
        
        for term in terms:
            if not term:
                continue
            
            t = term.lower()
            idx = text.find(t)
            
            while idx != -1:
                positions.append(idx)
                idx = text.find(t, idx + 1) 
        if len(positions) < 2:
            return False
        
        positions.sort()
        
        for i in range(1, len(positions)):
            if positions[i] - positions[i - 1] <= window:
                return True
                
        return False

    def rerank(self, queryTerms: List[str], hits: List[Hit], store: ChunkStore) -> List[Hit]:
       
        if not hits:
            return []
            
        reranked: List[Hit] = []

        for hit in hits:
            chunk: Chunk = store.get_chunk(hit.get_doc_id(), hit.get_chunk_id())
            
            if chunk is None:
                continue
            score: int = hit.get_score() * 10

            if queryTerms and len(queryTerms) >= 2:

                chunk_text_lower = chunk.get_text().lower()
                
                if self._any_terms_within_window(chunk_text_lower, queryTerms, self.__proximity_window):
                    score += self.__proximity_bonus

            doc_title: str = store.get_document_title(hit.get_doc_id())
            
            if doc_title:
               
                title_lower = doc_title.lower()
                
               
                for term in queryTerms:
                    if not term:
                        continue
                        
                    if term.lower() in title_lower:
                        score += self.__title_boost
                        break 
            reranked.append(Hit(hit.get_doc_id(), hit.get_chunk_id(), score))

        reranked.sort(key=lambda h: (
            -h.get_score(),           
            h.get_doc_id(),           
            h.get_chunk_id()         
        ))
        
        return reranked
