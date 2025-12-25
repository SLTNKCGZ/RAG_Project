import re
from typing import Dict, List, Set, Optional, Tuple

from src.model.intent import Intent
from src.writer.query_writer_abstract import QueryWriter
from src.writer.query_decomposer import QueryDecomposer
from src.writer.term_weighting import TermWeighting
from src.writer.simple_stemmer import SimpleStemmer


class HeuristicQueryWriter(QueryWriter):


    CLEAN_REGEX = r"[^A-Za-zÇĞİÖŞÜçğıöşü0-9 ]"
    SPLIT_REGEX = r"\s+"

    def __init__(
        self,
        stopwords: Optional[Set[str]],
        intent_boosters: Optional[Dict[Intent, List[str]]],
        enable_term_weighting: bool = True,
        enable_stemming: bool = True
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
        
        # Initialize QueryDecomposer for complex query handling
        self.__decomposer = QueryDecomposer()
        
        # Initialize Term Weighting
        self.__term_weighting = TermWeighting(
            tf_weight=1.0,      # Terim frekansı ağırlığı
            booster_weight=2.0, # Intent booster ağırlığı
            base_weight=1.0     # Temel ağırlık
        )
        self.__enable_term_weighting = enable_term_weighting
        
        # Initialize SimpleStemmer for lemmatization/stemming
        self.__stemmer = SimpleStemmer(min_word_length=3)
        self.__enable_stemming = enable_stemming

    
    def write(self, question: str, intent: Intent) -> List[str]:
        

        if question is None or question.strip() == "":
            return []

        # Step 1: Check if query is complex and decompose if necessary
        if self.__decomposer.is_complex_query(question):
            sub_queries = self.__decomposer.decompose(question)
            # Process each sub-query and combine results
            all_terms: List[str] = []
            for sub_query in sub_queries:
                terms = self._process_single_query(sub_query, intent)
                all_terms.extend(terms)
            # Remove duplicates while maintaining order
            unique_terms = list(dict.fromkeys(all_terms))
            return unique_terms
        else:
            # Simple query - process normally
            return self._process_single_query(question, intent)
    
    def _process_single_query(self, question: str, intent: Intent) -> List[str]:
        
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

        # Apply stemming if enabled (BEFORE adding boosters)
        if self.__enable_stemming:
            stemmed_terms = {}
            for term in ordered_terms.keys():
                stemmed_term = self.__stemmer.stem(term)
                stemmed_terms[stemmed_term] = None
            ordered_terms = stemmed_terms

        # Add boosters according to detected intent
        resolved_intent: Intent = intent if intent is not None else Intent.UNKNOWN
        boosters: List[str] = self.__intent_boosters.get(resolved_intent, [])

        # Stem boosters too for consistency
        if self.__enable_stemming:
            boosters = [self.__stemmer.stem(b) for b in boosters]

        for booster in boosters:
            ordered_terms[booster] = None

        # Convert back to ordered list
        terms = list(ordered_terms.keys())
        
        # Apply term weighting if enabled
        if self.__enable_term_weighting and terms:
            terms = self._apply_term_weighting(terms, boosters)
        
        return terms

    def _apply_term_weighting(self, terms: List[str], boosters: List[str]) -> List[str]:
        
        # Ağırlığa göre sırala
        ranked_terms = self.__term_weighting.rank_terms(terms, boosters)
        
        # Sadece terim adlarını döndür (ağırlık bilgisi hariç)
        weighted_terms = [term for term, _ in ranked_terms]
        
        return weighted_terms

    def get_term_weights(self, question: str, intent: Intent) -> Dict[str, float]:
        
        if question is None or question.strip() == "":
            return {}

        lower: str = question.lower()
        cleaned: str = re.sub(self.CLEAN_REGEX, " ", lower)
        parts: List[str] = re.split(self.SPLIT_REGEX, cleaned)

        ordered_terms: dict[str, None] = {}
        for p in parts:
            token: str = p.strip()
            if not token or token in self.__stopwords:
                continue
            ordered_terms[token] = None

        # Apply stemming if enabled
        if self.__enable_stemming:
            stemmed_terms = {}
            for term in ordered_terms.keys():
                stemmed_term = self.__stemmer.stem(term)
                stemmed_terms[stemmed_term] = None
            ordered_terms = stemmed_terms

        terms = list(ordered_terms.keys())
        resolved_intent: Intent = intent if intent is not None else Intent.UNKNOWN
        boosters: List[str] = self.__intent_boosters.get(resolved_intent, [])

        # Stem boosters too
        if self.__enable_stemming:
            boosters = [self.__stemmer.stem(b) for b in boosters]

        return self.__term_weighting.calculate_weights(terms, boosters)

    def get_stemming_stats(self, question: str) -> Dict[str, any]:
        """
        Stemming istatistiklerini döndürür (debug için).
        
        :param question: Sorgu metni.
        :return: Stemming istatistikleri.
        """
        if not self.__enable_stemming or question is None:
            return {}

        lower: str = question.lower()
        cleaned: str = re.sub(self.CLEAN_REGEX, " ", lower)
        parts: List[str] = re.split(self.SPLIT_REGEX, cleaned)

        terms = [p.strip() for p in parts if p.strip() and p.strip() not in self.__stopwords]
        
        return self.__stemmer.get_stats(terms)
