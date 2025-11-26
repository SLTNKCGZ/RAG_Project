from abc import ABC, abstractmethod
from src.model.intent import Intent
from typing import Optional


class IntentDetectorAbstract(ABC):
   
    @abstractmethod
    def detect(self, question: str) -> Intent:
        
        pass
