from typing import List, Dict, Optional

from src.model.query import Query
from src.model.intent import Intent
from src.model.hit import Hit
from src.model.answer import Answer
from src.data.chunk_store import ChunkStore


class Context:
    """
    Context object that holds all pipeline state.
    Acts as a central data carrier through the RAG pipeline stages.
    """
    
    def __init__(self):
        """Initialize Context with all attributes set to None."""
        self.question: Optional[Query] = None
        self.chunk_store: Optional[ChunkStore] = None
        self.intent: Optional[Intent] = None
        self.intent_keyword_rules: Optional[Dict[Intent, List[str]]] = None
        self.terms: Optional[List[str]] = None
        self.retrieved_hits: Optional[List[Hit]] = None
        self.reranked_hits: Optional[List[Hit]] = None
        self.final_answer: Optional[Answer] = None
    
    # Question methods
    def get_question(self) -> Optional[Query]:
        """Get the question."""
        return self.question
    
    def set_question(self, question: Query) -> None:
        """Set the question."""
        self.question = question
    
    # ChunkStore methods
    def get_chunk_store(self) -> Optional[ChunkStore]:
        """Get the chunk store."""
        return self.chunk_store
    
    def set_chunk_store(self, chunk_store: ChunkStore) -> None:
        """Set the chunk store."""
        self.chunk_store = chunk_store
    
    # Intent methods
    def get_intent(self) -> Optional[Intent]:
        """Get the detected intent."""
        return self.intent
    
    def set_intent(self, intent: Intent) -> None:
        """Set the detected intent."""
        self.intent = intent
    
    # Intent keyword rules methods
    def get_intent_keyword_rules(self) -> Optional[Dict[Intent, List[str]]]:
        """Get intent keyword rules mapping."""
        return self.intent_keyword_rules
    
    def set_intent_keyword_rules(self, rules: Dict[Intent, List[str]]) -> None:
        """Set intent keyword rules mapping."""
        self.intent_keyword_rules = rules
    
    # Query terms methods
    def get_terms(self) -> Optional[List[str]]:
        """Get query terms."""
        return self.terms
    
    def set_terms(self, terms: List[str]) -> None:
        """Set query terms."""
        self.terms = terms
    
    # Retrieved hits methods
    def get_retrieved_hits(self) -> Optional[List[Hit]]:
        """Get retrieved hits from retrieval stage."""
        return self.retrieved_hits
    
    def set_retrieved_hits(self, hits: List[Hit]) -> None:
        """Set retrieved hits."""
        self.retrieved_hits = hits
    
    # Reranked hits methods
    def get_reranked_hits(self) -> Optional[List[Hit]]:
        """Get reranked hits from reranking stage."""
        return self.reranked_hits
    
    def set_reranked_hits(self, hits: List[Hit]) -> None:
        """Set reranked hits."""
        self.reranked_hits = hits
    
    # Final answer methods
    def get_final_answer(self) -> Optional[Answer]:
        """Get the final generated answer."""
        return self.final_answer
    
    def set_final_answer(self, answer: Answer) -> None:
        """Set the final generated answer."""
        self.final_answer = answer
    
    def __repr__(self) -> str:
        return (f"Context(question={self.question is not None}, "
                f"chunk_store_size={self.chunk_store.size() if self.chunk_store else 0}, "
                f"intent={self.intent}, terms={len(self.terms) if self.terms else 0}, "
                f"retrieved_hits={len(self.retrieved_hits) if self.retrieved_hits else 0}, "
                f"reranked_hits={len(self.reranked_hits) if self.reranked_hits else 0}, "
                f"has_answer={self.final_answer is not None})")
