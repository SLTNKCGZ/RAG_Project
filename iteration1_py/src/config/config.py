from pathlib import Path
from typing import Optional


class Config:
    """
    Configuration object that holds all application settings.
    Stores pipeline types, parameters, and file paths.
    """
    
    def __init__(
        self,
        intent_type: str,
        writer_type: str,
        retriever_type: str,
        reranker_type: str,
        answer_agent_type: str,
        rules_file_path: Path,
        top_k: int,
        stopwords_file_path: Path,
        top_n: int,
        chunk_path: Path,
        logs_dir_path: Path
    ):
        """
        Initialize Config with all settings.
        
        Args:
            intent_type: Intent detector implementation type
            writer_type: Query writer implementation type
            retriever_type: Retriever implementation type
            reranker_type: Reranker implementation type
            answer_agent_type: Answer agent implementation type
            rules_file_path: Path to intent rules file
            top_k: Number of top hits to retrieve
            stopwords_file_path: Path to stopwords file
            top_n: Number of top query terms to use
            chunk_path: Path to chunk store file
            logs_dir_path: Path to logs directory
        """
        self.intent_type = intent_type
        self.writer_type = writer_type
        self.retriever_type = retriever_type
        self.reranker_type = reranker_type
        self.answer_agent_type = answer_agent_type
        self.rules_file_path = rules_file_path
        self.top_k = top_k
        self.stopwords_file_path = stopwords_file_path
        self.top_n = top_n
        self.chunk_path = chunk_path
        self.logs_dir_path = logs_dir_path
    
    def get_intent_type(self) -> str:
        """Get intent detector type."""
        return self.intent_type
    
    def get_writer_type(self) -> str:
        """Get query writer type."""
        return self.writer_type
    
    def get_retriever_type(self) -> str:
        """Get retriever type."""
        return self.retriever_type
    
    def get_reranker_type(self) -> str:
        """Get reranker type."""
        return self.reranker_type
    
    def get_answer_agent_type(self) -> str:
        """Get answer agent type."""
        return self.answer_agent_type
    
    def get_rules_file_path(self) -> Path:
        """Get rules file path."""
        return self.rules_file_path
    
    def get_top_k(self) -> int:
        """Get top K parameter."""
        return self.top_k
    
    def get_stopwords_file_path(self) -> Path:
        """Get stopwords file path."""
        return self.stopwords_file_path
    
    def get_top_n(self) -> int:
        """Get top N parameter."""
        return self.top_n
    
    def get_chunk_path(self) -> Path:
        """Get chunk store path."""
        return self.chunk_path
    
    def get_logs_dir_path(self) -> Path:
        """Get logs directory path."""
        return self.logs_dir_path
    
    def __repr__(self) -> str:
        return (f"Config(intent_type={self.intent_type}, writer_type={self.writer_type}, "
                f"retriever_type={self.retriever_type}, reranker_type={self.reranker_type}, "
                f"answer_agent_type={self.answer_agent_type}, top_k={self.top_k}, top_n={self.top_n})")
