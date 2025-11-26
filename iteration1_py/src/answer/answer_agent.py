from abc import ABC, abstractmethod
from typing import List
from src.model.hit import Hit
from src.model.answer import Answer
from src.data.chunk_store import ChunkStore


class AnswerAgent(ABC):
    @abstractmethod
    def answer(self, query: List[str], top_hits: List[Hit], chunk_store: ChunkStore) -> Answer:
        
        pass
