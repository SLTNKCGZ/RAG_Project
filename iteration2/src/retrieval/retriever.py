from abc import ABC, abstractmethod
from typing import List
from src.data.chunk_store import ChunkStore
from src.model.hit import Hit

class Retriever(ABC):

    @abstractmethod
    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
        pass
