import yaml
from pathlib import Path
from typing import Dict, List, Optional

from src.config.config import Config


class ConfigLoader:

    
    def __init__(self, config_path: Path):
        self.__config_path = Path(config_path)
    
    def load_config(self) -> Config:
        
        try:
            lines = self.__config_path.read_text(encoding="utf-8").splitlines()
            config_map = self.__parse_yaml(lines)

            # Extract values
            intent_type = config_map.get("pipeline.intent_detector")
            writer_type = config_map.get("pipeline.query_writer")
            retriever_type = config_map.get("pipeline.retriever")
            reranker_type = config_map.get("pipeline.reranker")
            answer_agent_type = config_map.get("pipeline.answer_agent")

            rules_file = config_map.get("params.intent.rules_file")
            top_k = int(config_map.get("params.retriever.top_k"))
            retriever_alpha = float(config_map.get("params.retriever.alpha", "0.5"))
            retriever_beta = float(config_map.get("params.retriever.beta", "0.5"))
            embedding_provider_type = config_map.get("params.embedding.provider", "SimpleEmbeddingProvider")
            stopwords_file = config_map.get("params.query_writer.stopwords_file")
            suffixes_file = config_map.get("params.query_writer.suffixes_file")
            conjunctions_file = config_map.get("params.query_writer.conjunctions_file")
            tf_weight = float(config_map.get("params.query_writer.tf_weight"))
            booster_weight = float(config_map.get("params.query_writer.booster_weight"))
            base_weight = float(config_map.get("params.query_writer.base_weight"))
            top_n = int(config_map.get("params.query_writer.top_n"))
            proximity_window = int(config_map.get("params.reranker.proximity_window", "15"))
            proximity_bonus = int(config_map.get("params.reranker.proximity_bonus", "5"))
            title_boost = int(config_map.get("params.reranker.title_boost", "3"))
            reranker_alpha = float(config_map.get("params.reranker.alpha", "0.5"))
            reranker_beta = float(config_map.get("params.reranker.beta", "0.5"))

            chunk_store = config_map.get("paths.chunk_store")
            logs_dir = config_map.get("paths.logs_dir")

            base_dir = self.__config_path.parent or self.__config_path.resolve().parent

            rules_path = self.__resolve_path(base_dir, rules_file)
            stopwords_path = self.__resolve_path(base_dir, stopwords_file)
            suffixes_path = self.__resolve_path(base_dir, suffixes_file)
            conjunctions_path = self.__resolve_path(base_dir, conjunctions_file)
            chunk_path = self.__resolve_path(base_dir, chunk_store)
            logs_path = self.__resolve_path(base_dir, logs_dir)
            
            return Config(
                intent_type=intent_type,
                writer_type=writer_type,
                retriever_type=retriever_type,
                reranker_type=reranker_type,
                answer_agent_type=answer_agent_type,
                rules_file_path=rules_path,
                top_k=int(top_k),
                retriever_alpha=retriever_alpha,
                retriever_beta=retriever_beta,
                embedding_provider_type=embedding_provider_type,
                stopwords_file_path=stopwords_path,
                suffixes_file_path=suffixes_path,
                conjunctions_file_path=conjunctions_path,
                tf_weight=tf_weight,
                booster_weight=booster_weight,
                base_weight=base_weight,
                top_n=int(top_n),
                proximity_window=proximity_window,
                proximity_bonus=proximity_bonus,
                title_boost=title_boost,
                reranker_alpha=reranker_alpha,
                reranker_beta=reranker_beta,
                chunk_path=chunk_path,
                logs_dir_path=logs_path
            )
        
        
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.__config_path}: {e}")
    


    def __parse_yaml(self, lines: List[str]) -> Dict[str, str]:
        map_data: Dict[str, str] = {}
        section = None
        subsection = None

        for line in lines:
            if line.strip() == "" or line.strip().startswith("#"):
                continue

            indent = self.__get_indent_level(line)
            content = line.strip()

            # Section or subsection
            if content.endswith(":") and not ":" in content[:-1]:
                name = content[:-1]

                if indent == 0:
                    section = name
                    subsection = None
                elif indent == 2 and section is not None:
                    subsection = f"{section}.{name}"

                continue

            # Key-value
            if ":" in content:
                key, value = content.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"')

                if indent == 4 and subsection:
                    full_key = f"{subsection}.{key}"
                elif indent == 2 and section:
                    full_key = f"{section}.{key}"
                else:
                    full_key = key

                map_data[full_key] = value

        return map_data

    def __get_indent_level(self, line: str) -> int:
        count = 0
        for c in line:
            if c == " ":
                count += 1
            else:
                break
        return count

    def __resolve_path(self, base_dir: Path, raw: Optional[str]) -> Path:
        if not raw:
            raise ValueError("Raw path is None")

        raw_path = Path(raw)

        if raw_path.is_absolute():
            return raw_path.resolve()

        # Clean "./"
        if raw.startswith("./"):
            raw = raw[2:]

        # Resolve "../"
        resolved = base_dir
        while raw.startswith("../"):
            resolved = resolved.parent
            raw = raw[3:]

        return (resolved / raw).resolve()
