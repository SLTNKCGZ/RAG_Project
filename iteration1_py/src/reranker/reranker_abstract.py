from abc import ABC, abstractmethod
from typing import List
from data.chunk_store import ChunkStore
from model.hit import Hit

class Reranker(ABC):

    @abstractmethod
    def rerank(self, query: List[str], hits: List[Hit], store: ChunkStore) -> List[Hit]:
        pass
