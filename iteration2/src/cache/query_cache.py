import json
from pathlib import Path
from typing import Dict, Any, Optional

from src.model.answer import Answer


class QueryCache:

    def __init__(self, cache_file_path: Path, max_size: int = 100):
        self.__cache_file_path = Path(cache_file_path)
        self.__cache: Dict[str, Dict[str, Any]] = {}
        self.__max_size = max_size
        self._load_from_file()

    def _load_from_file(self) -> None:
        if self.__cache_file_path.exists():
            try:
                with open(self.__cache_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.__cache = data
            except (json.JSONDecodeError, IOError):
                self.__cache = {}

    def _save_to_file(self) -> None:
        try:
            self.__cache_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.__cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.__cache, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def get(self, query: str) -> Optional[Answer]:
        query_lower = query.lower()
        cached_data = self.__cache.get(query_lower)

        if cached_data is None:
            return None

        return Answer(
            text=cached_data.get("text", ""),
            citations=cached_data.get("citations", [])
        )

    def set(self, query: str, answer: Answer) -> None:
        query_lower = query.lower()

        if len(self.__cache) >= self.__max_size:
            first_key = next(iter(self.__cache))
            del self.__cache[first_key]

        self.__cache[query_lower] = {
            "text": answer.get_text(),
            "citations": answer.get_citations()
        }

        self._save_to_file()

