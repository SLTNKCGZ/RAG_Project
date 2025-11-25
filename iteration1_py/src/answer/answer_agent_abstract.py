from abc import ABC, abstractmethod
from typing import List
from src.model.hit import Hit
from src.model.answer import Answer
from src.data.chunk_store import ChunkStore


class AnswerAgentAbstract(ABC):
    """
    Strategy interface for answer generation
    SOLID: DIP - Depend on abstraction
    Design Pattern: Strategy
    """

    @abstractmethod
    def answer(self, query: List[str], top_hits: List[Hit], chunk_store: ChunkStore) -> Answer:
        """
        Generate answer from top hits
        
        Args:
            query: The query terms
            top_hits: The top retrieved and reranked hits
            chunk_store: The chunk store for reference
            
        Returns:
            Answer with text and citations
        """
        pass
