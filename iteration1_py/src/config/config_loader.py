import yaml
from pathlib import Path
from typing import Dict, Optional

from src.config.config import Config


class ConfigLoader:
    """
    Loads configuration from YAML file.
    Parses the config.yaml file and creates a Config object.
    """
    
    def __init__(self, config_path: Path):
        """
        Initialize ConfigLoader.
        
        Args:
            config_path: Path to the config.yaml file
        """
        self.config_path = Path(config_path)
    
    def load_config(self) -> Config:
        """
        Load and parse configuration from YAML file.
        
        Returns:
            Config object with parsed settings
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is malformed
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            if not config_data:
                raise ValueError("Config file is empty")
            
            # Extract pipeline configuration
            pipeline = config_data.get('pipeline', {})
            intent_type = pipeline.get('intent_detector', 'RuleIntentDetector')
            writer_type = pipeline.get('query_writer', 'HeuristicQueryWriter')
            retriever_type = pipeline.get('retriever', 'KeywordRetriever')
            reranker_type = pipeline.get('reranker', 'SimpleReranker')
            answer_agent_type = pipeline.get('answer_agent', 'TemplateAnswerAgent')
            
            # Extract parameters
            params = config_data.get('params', {})
            
            intent_params = params.get('intent', {})
            rules_file = intent_params.get('rules_file', 'resources/intent_rules.yaml')
            
            retriever_params = params.get('retriever', {})
            top_k = retriever_params.get('top_k', 5)
            
            writer_params = params.get('query_writer', {})
            stopwords_file = writer_params.get('stopwords_file', 'resources/stopwords.yaml')
            top_n = writer_params.get('top_n', 3)
            
            # Extract paths
            paths = config_data.get('paths', {})
            chunk_store = paths.get('chunk_store', 'data/chunks.json')
            logs_dir = paths.get('logs_dir', 'logs')
            
            # Resolve paths relative to config file directory
            base_dir = self.config_path.parent
            rules_file_path = self._resolve_path(base_dir, rules_file)
            stopwords_file_path = self._resolve_path(base_dir, stopwords_file)
            chunk_path = self._resolve_path(base_dir, chunk_store)
            logs_dir_path = self._resolve_path(base_dir, logs_dir)
            
            return Config(
                intent_type=intent_type,
                writer_type=writer_type,
                retriever_type=retriever_type,
                reranker_type=reranker_type,
                answer_agent_type=answer_agent_type,
                rules_file_path=rules_file_path,
                top_k=int(top_k),
                stopwords_file_path=stopwords_file_path,
                top_n=int(top_n),
                chunk_path=chunk_path,
                logs_dir_path=logs_dir_path
            )
        
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML config: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.config_path}: {e}")
    
    @staticmethod
    def _resolve_path(base_dir: Path, relative_path: str) -> Path:
        """
        Resolve a path relative to base directory.
        If path is absolute, return as-is.
        
        Args:
            base_dir: Base directory for relative paths
            relative_path: Path to resolve
            
        Returns:
            Resolved absolute Path
        """
        path = Path(relative_path)
        
        if path.is_absolute():
            return path
        
        return (base_dir / path).resolve()
