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
        suffixes: List[str],
        conjunctions: List[str],
        tf_weight: float,
        booster_weight: float,
        base_weight: float,
        enable_term_weighting: bool = True,
        enable_stemming: bool = True
    ) -> None:

        if stopwords is None:
            self.__stopwords: Set[str] = set()
        else:
            self.__stopwords = {
                s.lower() for s in stopwords
                if s is not None and s.strip() != ""
            }

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

        self.__decomposer = QueryDecomposer(conjunctions)
        self.__term_weighting = TermWeighting(
            tf_weight=tf_weight,
            booster_weight=booster_weight,
            base_weight=base_weight
        )
        self.__enable_term_weighting = enable_term_weighting
        self.__stemmer = SimpleStemmer(suffixes=suffixes, min_word_length=3)
        self.__enable_stemming = enable_stemming

    def write(self, question: str, intent: Intent) -> List[str]:
        if question is None or question.strip() == "":
            return []

        if self.__decomposer.is_complex_query(question):
            sub_queries = self.__decomposer.decompose(question)
            all_terms: List[str] = []
            for sub_query in sub_queries:
                terms = self._process_single_query(sub_query, intent)
                all_terms.extend(terms)
            return list(dict.fromkeys(all_terms))
        else:
            return self._process_single_query(question, intent)

    def _process_single_query(self, question: str, intent: Intent) -> List[str]:
        if question is None or question.strip() == "":
            return []

        lower: str = question.lower()
        cleaned: str = re.sub(self.CLEAN_REGEX, " ", lower)
        parts: List[str] = re.split(self.SPLIT_REGEX, cleaned)

        ordered_terms: dict[str, None] = {}
        for p in parts:
            token: str = p.strip()
            if not token or token in self.__stopwords:
                continue
            ordered_terms[token] = None

        if self.__enable_stemming:
            stemmed_terms = {}
            for term in ordered_terms.keys():
                stemmed_term = self.__stemmer.stem(term)
                stemmed_terms[stemmed_term] = None
            ordered_terms = stemmed_terms

        resolved_intent: Intent = intent if intent is not None else Intent.UNKNOWN
        boosters: List[str] = self.__intent_boosters.get(resolved_intent, [])

        if self.__enable_stemming:
            boosters = [self.__stemmer.stem(b) for b in boosters]

        for booster in boosters:
            ordered_terms[booster] = None

        terms = list(ordered_terms.keys())

        if self.__enable_term_weighting and terms:
            terms = self._apply_term_weighting(terms, boosters)

        return terms

    def _apply_term_weighting(self, terms: List[str], boosters: List[str]) -> List[str]:
        ranked_terms = self.__term_weighting.rank_terms(terms, boosters)
        return [term for term, _ in ranked_terms]
