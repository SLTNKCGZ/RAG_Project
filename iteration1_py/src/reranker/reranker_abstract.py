from abc import ABC, abstractmethod
from typing import List
from src.model.hit import Hit
from src.data.chunk_store import ChunkStore


class RerankerAbstract(ABC):

    @abstractmethod
    def rerank(self, query: List[str], hits: List[Hit], store: ChunkStore) -> List[Hit]:
        
        pass
