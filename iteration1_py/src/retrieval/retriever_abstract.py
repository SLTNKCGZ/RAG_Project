from abc import ABC, abstractmethod
from typing import List
from data.chunk_store import ChunkStore
from model.hit import Hit

class Retriever(ABC):

    @abstractmethod
    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
        pass
