from abc import ABC, abstractmethod
from typing import List
from src.model.intent import Intent


class QueryWriterAbstract(ABC):
   
    @abstractmethod
    def write(self, question: str, intent: Intent) -> List[str]:
       
        pass
