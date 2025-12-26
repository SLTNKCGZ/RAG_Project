from abc import ABC, abstractmethod
from typing import List, Set, Dict
from pathlib import Path
import time

from src.config.config import Config
from src.context.context import Context
from src.trace.trace_bus import TraceBus
from src.trace.trace_event import TraceEvent
from src.model.intent import Intent
from src.model.hit import Hit
from src.model.answer import Answer


class RagPipeline(ABC):
    
    def __init__(self, config: Config, context: Context, trace_bus: TraceBus):
        self._config = config
        self._context = context
        self._trace_bus = trace_bus
        
        self._intent_detector = None
        self._query_writer = None
        self._retriever = None
        self._reranker = None
        self._answer_agent = None
        self._vector_index = None
    
    @abstractmethod
    def execute(self) -> None:
        pass
    
    def detect_intent(self) -> None:
        start_time = time.time()
        question = self._context.get_question().get_text()
        inputs = f'question="{question}"'
        outputs_summary = ""
        error = None
        
        try:
            from src.intent.intent_rules_loader import IntentRulesLoader
            from src.intent.rule_intent_detector import RuleIntentDetector
            
            if self._config.get_intent_type() == "RuleIntentDetector":
                rules_loader = IntentRulesLoader()
                rules = rules_loader.load_rules(self._config.get_rules_file_path())
                priority_order = list(rules.keys())
                self._intent_detector = RuleIntentDetector(rules, priority_order)
                self._context.set_intent_keyword_rules(rules)
            else:
                raise IllegalArgumentError(f"Unknown intent detector type: {self._config.get_intent_type()}")
            
            intent = self._intent_detector.detect(question)
            self._context.set_intent(intent)
            outputs_summary = f"intent={intent}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self._trace_bus.publish(TraceEvent("detectIntent", inputs, outputs_summary, timing_ms, error))
    
    def write_query(self) -> None:
        start_time = time.time()
        question = self._context.get_question().get_text()
        inputs = ""
        outputs_summary = ""
        error = None
        
        try:
            from src.writer.heuristic_query_writer import HeuristicQueryWriter

            if self._config.get_writer_type() == "HeuristicQueryWriter":
                stopwords = self.load_stopwords(self._config.get_stopwords_file_path())
                suffixes = self.load_suffixes(self._config.get_suffixes_file_path())
                conjunctions = self.load_conjunctions(self._config.get_conjunctions_file_path())
                inputs = f"stopwords={len(stopwords)} stopwords{stopwords}"
                boosters = self._context.get_intent_keyword_rules()
                if boosters is None:
                    boosters = {}
                self._query_writer = HeuristicQueryWriter(
                    stopwords,
                    boosters,
                    suffixes,
                    conjunctions,
                    self._config.get_tf_weight(),
                    self._config.get_booster_weight(),
                    self._config.get_base_weight()
                )
            else:
                raise IllegalArgumentError(f"Unknown query writer type: {self._config.get_writer_type()}")
            
            terms = self._query_writer.write(question, self._context.get_intent())
            self._context.set_terms(terms)
            outputs_summary = f"Number of terms: {len(terms)} Terms:{terms}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self._trace_bus.publish(TraceEvent("writeQuery", inputs, outputs_summary, timing_ms, error))
    
    def retrieve(self) -> None:
        start_time = time.time()
        terms = self._context.get_terms()
        inputs = f"Size of terms {len(terms)} Terms: {terms}"
        outputs_summary = ""
        error = None
        
        try:
            from src.retrieval.keyword_retriever import KeywordRetriever
            from src.retrieval.vector_retriver import VectorRetriever
            from src.retrieval.hybrid_retriever import HybridRetriever
            from src.index.vector_index import VectorIndex
            from src.embedding.simple_embedding_provider import SimpleEmbeddingProvider
            from src.writer.simple_stemmer import SimpleStemmer
            
            retriever_type = self._config.get_retriever_type()
            chunk_store = self._context.get_chunk_store()
            suffixes = self.load_suffixes(self._config.get_suffixes_file_path())
            stemmer = SimpleStemmer(suffixes=suffixes, min_word_length=3)
            
            if retriever_type == "KeywordRetriever":
                self._retriever = KeywordRetriever(self._config.get_top_k(), stemmer)
            elif retriever_type == "VectorRetriever":
                if self._vector_index is None:
                    embedding_provider = SimpleEmbeddingProvider()
                    self._vector_index = VectorIndex(chunk_store, embedding_provider)
                self._retriever = VectorRetriever(self._vector_index, self._config.get_top_k())
            elif retriever_type == "HybridRetriever":
                keyword_retriever = KeywordRetriever(self._config.get_top_k(), stemmer)
                if self._vector_index is None:
                    embedding_provider = SimpleEmbeddingProvider()
                    self._vector_index = VectorIndex(chunk_store, embedding_provider)
                vector_retriever = VectorRetriever(self._vector_index, self._config.get_top_k())
                self._retriever = HybridRetriever(
                    keyword_retriever,
                    vector_retriever,
                    self._config.get_retriever_alpha(),
                    self._config.get_retriever_beta(),
                    self._config.get_top_k()
                )
            else:
                raise IllegalArgumentError(f"Unknown retriever type: {retriever_type}")
            
            hits = self._retriever.retrieve(terms, chunk_store)
            self._context.set_retrieved_hits(hits)
            outputs_summary = f"Number of hits: {len(hits)} retrievedHits: {hits}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self._trace_bus.publish(TraceEvent("retrieve", inputs, outputs_summary, timing_ms, error))
    
    def rerank(self) -> None:
        
        start_time = time.time()
        terms = self._context.get_terms()
        hits = self._context.get_retrieved_hits()
        inputs = f"Size of retrievedHits: {len(hits)} Hits: {hits}"
        outputs_summary = ""
        error = None
        
        try:
            from src.reranker.simple_reranker import SimpleReranker
            from src.reranker.cosine_reranker import CosineReranker
            from src.reranker.hybrid_reranker import HybridReranker
            
            reranker_type = self._config.get_reranker_type()
            
            if reranker_type == "SimpleReranker":
                self._reranker = SimpleReranker(
                    self._config.get_proximity_window(),
                    self._config.get_proximity_bonus(),
                    self._config.get_title_boost()
                )
            elif reranker_type == "CosineReranker":
                self._reranker = CosineReranker()
            elif reranker_type == "HybridReranker":
                self._reranker = HybridReranker(
                    self._config.get_reranker_alpha(),
                    self._config.get_reranker_beta()
                )
            else:
                raise IllegalArgumentError(f"Unknown reranker type: {reranker_type}")
            
            reranked_hits = self._reranker.rerank(terms, hits, self._context.get_chunk_store())
            self._context.set_reranked_hits(reranked_hits)
            outputs_summary = f"Size of rerankedHits: {len(reranked_hits)} hits: {reranked_hits}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self._trace_bus.publish(TraceEvent("rerank", inputs, outputs_summary, timing_ms, error))
    
    def answer(self) -> None:
        start_time = time.time()
        reranked_hits = self._context.get_reranked_hits()
        inputs = f"Number of hits: {len(reranked_hits)} rerankedHits: {reranked_hits}"
        outputs_summary = ""
        error = None
        
        try:
            from src.answer.template_answer_agent import TemplateAnswerAgent
            
            if self._config.get_answer_agent_type() == "TemplateAnswerAgent":
                self._answer_agent = TemplateAnswerAgent()
            else:
                raise IllegalArgumentError(f"Unknown answer agent type: {self._config.get_answer_agent_type()}")
            
            query_terms = self._context.get_terms()
            generated_answer = self._answer_agent.answer(query_terms, reranked_hits, self._context.get_chunk_store())
            self._context.set_final_answer(generated_answer)
            outputs_summary = f"Answer: {generated_answer}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self._trace_bus.publish(TraceEvent("answer", inputs, outputs_summary, timing_ms, error))
    
    def load_stopwords(self, stopwords_path: Path) -> Set[str]:
        try:
            stopwords = set()
            in_stopwords = False
            
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                for line in f:
                    trimmed = line.strip()
                    
                    if not trimmed or trimmed.startswith("#"):
                        continue
                    
                    if trimmed == "stop_words:":
                        in_stopwords = True
                        continue
                    
                    if in_stopwords and trimmed.startswith("-"):
                        word = trimmed[1:].strip()
                        if word.startswith('"') and word.endswith('"'):
                            word = word[1:-1]
                        stopwords.add(word)
            
            return stopwords
        except Exception as e:
            raise RuntimeError(f"Failed to load stopwords from: {stopwords_path}") from e

    def load_suffixes(self, suffixes_path: Path) -> List[str]:
        try:
            suffixes = []
            in_suffixes = False
            
            with open(suffixes_path, 'r', encoding='utf-8') as f:
                for line in f:
                    trimmed = line.strip()
                    
                    if not trimmed or trimmed.startswith("#"):
                        continue
                    
                    if trimmed == "suffixes:":
                        in_suffixes = True
                        continue
                    
                    if in_suffixes and trimmed.startswith("-"):
                        suffix = trimmed[1:].strip()
                        if suffix.startswith('"') and suffix.endswith('"'):
                            suffix = suffix[1:-1]
                        suffixes.append(suffix)
            
            return suffixes
        except Exception as e:
            raise RuntimeError(f"Failed to load suffixes from: {suffixes_path}") from e

    def load_conjunctions(self, conjunctions_path: Path) -> List[str]:
        try:
            conjunctions = []
            in_conjunctions = False
            
            with open(conjunctions_path, 'r', encoding='utf-8') as f:
                for line in f:
                    trimmed = line.strip()
                    
                    if not trimmed or trimmed.startswith("#"):
                        continue
                    
                    if trimmed == "conjunctions:":
                        in_conjunctions = True
                        continue
                    
                    if in_conjunctions and trimmed.startswith("-"):
                        conjunction = trimmed[1:].strip()
                        if conjunction.startswith('"') and conjunction.endswith('"'):
                            conjunction = conjunction[1:-1]
                        conjunctions.append(conjunction)
            
            return conjunctions
        except Exception as e:
            raise RuntimeError(f"Failed to load conjunctions from: {conjunctions_path}") from e


class IllegalArgumentError(Exception):
    pass
