from abc import ABC, abstractmethod
from typing import List
from src.model.hit import Hit
from src.data.chunk_store import ChunkStore


class RetrieverAbstract(ABC):
    

    @abstractmethod
    def retrieve(self, query_terms: List[str], store: ChunkStore) -> List[Hit]:
       
        pass
