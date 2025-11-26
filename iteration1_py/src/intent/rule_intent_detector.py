from typing import Dict, List
from models import Intent
from chunk_store import ChunkStore   # Eğer gerekirse, kullanılmasa bile import sorun olmaz
from intent_detector import IntentDetector


class RuleIntentDetector(IntentDetector):
  

    def __init__(
        self,
        rules: Dict[Intent, List[str]],
        priority_order: List[Intent]
    ) -> None:
    
        self.rules: Dict[Intent, List[str]] = rules
        self.priority_order: List[Intent] = priority_order

    def detect(self, question: str) -> Intent:
      
        if question is None or question.strip() == "":
            return Intent.Unknown

        lower: str = question.lower()

        # Check intents in priority order (same logic as Java)
        for intent in self.priority_order:
            keywords: List[str] = self.rules.get(intent, [])

            for keyword in keywords:
                if keyword and keyword.lower() in lower:
                    return intent

        return Intent.Unknown
