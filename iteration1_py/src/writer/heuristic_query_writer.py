import re
from typing import Dict, List, Set, Optional

from src.model.intent import Intent
from src.writer.query_writer_abstract import QueryWriter


class HeuristicQueryWriter(QueryWriter):


    # TR locale pattern is approximated because Python locale lowercasing differs
    CLEAN_REGEX = r"[^A-Za-zÇĞİÖŞÜçğıöşü0-9 ]"
    SPLIT_REGEX = r"\s+"

    def __init__(
        self,
        stopwords: Optional[Set[str]],
        intent_boosters: Optional[Dict[Intent, List[str]]]
    ) -> None:

        # Normalize stopwords
        if stopwords is None:
            self.__stopwords: Set[str] = set()
        else:
            self.__stopwords = {
                s.lower() for s in stopwords
                if s is not None and s.strip() != ""
            }

        # Normalize boosters
        if intent_boosters is None:
            self.__intent_boosters: Dict[Intent, List[str]] = {}
        else:
            normalized: Dict[Intent, List[str]] = {}

            for intent, tokens in intent_boosters.items():
                clean_tokens: List[str] = [
                    t.lower()
                    for t in tokens
                    if t is not None and t.strip() != ""
                ]
                normalized[intent] = clean_tokens

            self.__intent_boosters = normalized

    
    def write(self, question: str, intent: Intent) -> List[str]:
        

        if question is None or question.strip() == "":
            return []

        # Lowercase & clean unwanted characters
        lower: str = question.lower()
        cleaned: str = re.sub(self.CLEAN_REGEX, " ", lower)

        # Tokenize
        parts: List[str] = re.split(self.SPLIT_REGEX, cleaned)

        # Ordered unique tokens (LinkedHashSet equivalent)
        ordered_terms: dict[str, None] = {}

        for p in parts:
            token: str = p.strip()
            if not token:
                continue
            if token in self.__stopwords:
                continue
            ordered_terms[token] = None

        # Add boosters according to detected intent
        resolved_intent: Intent = intent if intent is not None else Intent.UNKNOWN
        boosters: List[str] = self.__intent_boosters.get(resolved_intent, [])

        for booster in boosters:
            ordered_terms[booster] = None

        # Convert back to ordered list
        return list(ordered_terms.keys())
