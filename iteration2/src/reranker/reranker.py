from abc import ABC, abstractmethod
from typing import List

from src.data.chunk_store import ChunkStore
from src.model.hit import Hit

class Reranker(ABC):

    @abstractmethod
    def rerank(self, query: List[str], hits: List[Hit], store: ChunkStore) -> List[Hit]:
        pass
