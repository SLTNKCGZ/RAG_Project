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
        
        self.__config = config
        self.__context = context
        self.__trace_bus = trace_bus
        
        self.__intent_detector = None
        self.__query_writer = None
        self.__retriever = None
        self.__reranker = None
        self.__answer_agent = None
    
    @abstractmethod
    def execute(self) -> None:
        pass
    
    def detect_intent(self) -> None:
        start_time = time.time()
        question = self.__context.get_question().get_text()
        inputs = f'question="{question}"'
        outputs_summary = ""
        error = None
        
        try:
            from src.intent.intent_rules_loader import IntentRulesLoader
            from src.intent.rule_intent_detector import RuleIntentDetector
            
            if self.__config.get_intent_type() == "RuleIntentDetector":
                rules_loader = IntentRulesLoader()
                rules = rules_loader.load_rules(self.__config.get_rules_file_path())
                priority_order = list(rules.keys())
                self._intent_detector = RuleIntentDetector(rules, priority_order)
                self.__context.set_intent_keyword_rules(rules)
            else:
                raise IllegalArgumentError(f"Unknown intent detector type: {self.__config.get_intent_type()}")
            
            intent = self._intent_detector.detect(question)
            self.__context.set_intent(intent)
            outputs_summary = f"intent={intent}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self.__trace_bus.publish(TraceEvent("detectIntent", inputs, outputs_summary, timing_ms, error))
    
    def write_query(self) -> None:
        start_time = time.time()
        question = self.__context.get_question().get_text()
        inputs = ""
        outputs_summary = ""
        error = None
        
        try:
            from src.writer.heuristic_query_writer import HeuristicQueryWriter
            
            if self.__config.get_writer_type() == "HeuristicQueryWriter":
                stopwords = self.load_stopwords(self.__config.get_stopwords_file_path())
                inputs = f"stopwords={len(stopwords)} stopwords{stopwords}"
                boosters = self.__context.get_intent_keyword_rules()
                if boosters is None:
                    boosters = {}
                self._query_writer = HeuristicQueryWriter(stopwords, boosters)
            else:
                raise IllegalArgumentError(f"Unknown query writer type: {self.__config.get_writer_type()}")
            
            terms = self._query_writer.write(question, self.__context.get_intent())
            self.__context.set_terms(terms)
            outputs_summary = f"Number of terms: {len(terms)} Terms:{terms}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self.__trace_bus.publish(TraceEvent("writeQuery", inputs, outputs_summary, timing_ms, error))
    
    def retrieve(self) -> None:
        start_time = time.time()
        terms = self.__context.get_terms()
        inputs = f"Size of terms {len(terms)} Terms: {terms}"
        outputs_summary = ""
        error = None
        
        try:
            from src.retrieval.keyword_retriever import KeywordRetriever
            
            if self.__config.get_retriever_type() == "KeywordRetriever":
                self._retriever = KeywordRetriever(self.__config.get_top_k())
            else:
                raise IllegalArgumentError(f"Unknown retriever type: {self.__config.get_retriever_type()}")
            
            hits = self._retriever.retrieve(terms, self.__context.get_chunk_store())
            self.__context.set_retrieved_hits(hits)
            outputs_summary = f"Number of hits: {len(hits)} retrievedHits: {hits}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self.__trace_bus.publish(TraceEvent("retrieve", inputs, outputs_summary, timing_ms, error))
    
    def rerank(self) -> None:
        
        start_time = time.time()
        terms = self.__context.get_terms()
        hits = self.__context.get_retrieved_hits()
        inputs = f"Size of retrievedHits: {len(hits)} Hits: {hits}"
        outputs_summary = ""
        error = None
        
        try:
            from src.reranker.simple_reranker import SimpleReranker
            from src.data.chunk_loader import ChunkLoader
            
            if self.__config.get_reranker_type() == "SimpleReranker":
                proximity_window = 15
                proximity_bonus = 5
                title_boost = 3
                self._reranker = SimpleReranker(proximity_window, proximity_bonus, title_boost)
            else:
                raise IllegalArgumentError(f"Unknown reranker type: {self.__config.get_reranker_type()}")
            
            chunk_loader = ChunkLoader()
            chunk_store = chunk_loader.load_chunks(self.__config.get_chunk_path())
            
            reranked_hits = self._reranker.rerank(terms, hits, chunk_store)
            self.__context.set_reranked_hits(reranked_hits)
            outputs_summary = f"Size of rerankedHits: {len(reranked_hits)} hits: {reranked_hits}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self.__trace_bus.publish(TraceEvent("rerank", inputs, outputs_summary, timing_ms, error))
    
    def answer(self) -> None:
        start_time = time.time()
        reranked_hits = self.__context.get_reranked_hits()
        inputs = f"Number of hits: {len(reranked_hits)} rerankedHits: {reranked_hits}"
        outputs_summary = ""
        error = None
        
        try:
            from src.answer.template_answer_agent import TemplateAnswerAgent
            
            if self.__config.get_answer_agent_type() == "TemplateAnswerAgent":
                self._answer_agent = TemplateAnswerAgent()
            else:
                raise IllegalArgumentError(f"Unknown answer agent type: {self.__config.get_answer_agent_type()}")
            
            query_terms = self.__context.get_terms()
            generated_answer = self._answer_agent.answer(query_terms, reranked_hits, self.__context.get_chunk_store())
            self.__context.set_final_answer(generated_answer)
            outputs_summary = f"Answer: {generated_answer}"
        except Exception as e:
            error = str(e)
            raise
        finally:
            timing_ms = (time.time() - start_time) * 1000
            self.__trace_bus.publish(TraceEvent("answer", inputs, outputs_summary, timing_ms, error))
    
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


class IllegalArgumentError(Exception):
    pass
