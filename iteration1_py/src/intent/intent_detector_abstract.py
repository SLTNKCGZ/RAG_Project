from abc import ABC, abstractmethod
from src.model.intent import Intent


class IntentDetectorAbstract(ABC):
   
    @abstractmethod
    def detect(self, question: str) -> Intent:
        
        pass
