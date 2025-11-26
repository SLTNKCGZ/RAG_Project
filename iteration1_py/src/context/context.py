from typing import List, Dict
from src.model.query import Query
from src.model.intent import Intent
from src.model.hit import Hit
from src.model.answer import Answer
from src.data.chunk_store import ChunkStore

class Context:
    def __init__(self) -> None:
        self.__question: Query = None
        self.__chunk_store: ChunkStore = None
        self.__intent: Intent = None
        self.__intent_keyword_rules: Dict[Intent, List[str]] = None
        self.__terms: List[str] = None
        self.__retrieved_hits: List[Hit] = None
        self.__reranked_hits: List[Hit] = None
        self.__final_answer: Answer = None

    # Question
    def get_question(self) -> Query:
        return self.__question

    def set_question(self, value: Query) -> None:
        self.__question = value

    # ChunkStore
    def get_chunk_store(self) -> ChunkStore:
        return self.__chunk_store

    def set_chunk_store(self, value: ChunkStore) -> None:
        self.__chunk_store = value

    # Intent
    def get_intent(self) -> Intent:
        return self.__intent

    def set_intent(self, value: Intent) -> None:
        self.__intent = value

    # Intent keyword rules
    def get_intent_keyword_rules(self) -> Dict[Intent, List[str]]:
        return self.__intent_keyword_rules

    def set_intent_keyword_rules(self, value: Dict[Intent, List[str]]) -> None:
        self.__intent_keyword_rules = value

    # Terms
    def get_terms(self) -> List[str]:
        return self.__terms

    def set_terms(self, value: List[str]) -> None:
        self.__terms = value

    # Retrieved hits
    def get_retrieved_hits(self) -> List[Hit]:
        return self.__retrieved_hits

    def set_retrieved_hits(self, value: List[Hit]) -> None:
        self.__retrieved_hits = value

    # Reranked hits
    def get_reranked_hits(self) -> List[Hit]:
        return self.__reranked_hits

    def set_reranked_hits(self, value: List[Hit]) -> None:
        self.__reranked_hits = value

    # Final answer
    def get_final_answer(self) -> Answer:
        return self.__final_answer

    def set_final_answer(self, value: Answer) -> None:
        self.__final_answer = value
