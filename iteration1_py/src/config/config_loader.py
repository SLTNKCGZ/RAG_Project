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
            stopwords_file = config_map.get("params.query_writer.stopwords_file")
            top_n = int(config_map.get("params.query_writer.top_n"))

            chunk_store = config_map.get("paths.chunk_store")
            logs_dir = config_map.get("paths.logs_dir")

            base_dir = self.__config_path.parent or self.__config_path.resolve().parent

            rules_path = self.__resolve_path(base_dir, rules_file)
            stopwords_path = self.__resolve_path(base_dir, stopwords_file)
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
                stopwords_file_path=stopwords_path,
                top_n=int(top_n),
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
