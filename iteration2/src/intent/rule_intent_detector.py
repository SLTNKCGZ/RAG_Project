from typing import Dict, List

from src.model.intent import Intent
from src.intent.intent_detector import IntentDetector


class RuleIntentDetector(IntentDetector):
  

    def __init__(self, rules: Dict[Intent, List[str]], priority_order: List[Intent]) -> None:
        self.__rules: Dict[Intent, List[str]] = rules
        self.__priority_order: List[Intent] = priority_order
    
    def detect(self, question: str) -> Intent:
        if question is None or question.strip() == "":
            return Intent.UNKNOWN

        lower: str = question.lower()

        # Check intents in priority order (same logic as Java)
        for intent in self.__priority_order:
            keywords: List[str] = self.__rules.get(intent, [])

            for keyword in keywords:
                if keyword and keyword.lower() in lower:
                    return intent

        return Intent.UNKNOWN
