from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from data.chunk_store import ChunkStore 
    from model.hit import Hit

class Reranker(ABC):

    @abstractmethod
    def rerank(self, query: List[str], hits: List[Hit], store: 'ChunkStore') -> List['Hit']:
        pass
