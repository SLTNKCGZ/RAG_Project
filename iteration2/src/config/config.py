from pathlib import Path

class Config:
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
        self.__intent_type = intent_type
        self.__writer_type = writer_type
        self.__retriever_type = retriever_type
        self.__reranker_type = reranker_type
        self.__answer_agent_type = answer_agent_type
        self.__rules_file_path = rules_file_path
        self.__top_k = top_k
        self.__stopwords_file_path = stopwords_file_path
        self.__top_n = top_n
        self.__chunk_path = chunk_path
        self.__logs_dir_path = logs_dir_path

    # Getters
    def get_intent_type(self) -> str:
        return self.__intent_type

    def get_writer_type(self) -> str:
        return self.__writer_type

    def get_retriever_type(self) -> str:
        return self.__retriever_type

    def get_reranker_type(self) -> str:
        return self.__reranker_type

    def get_answer_agent_type(self) -> str:
        return self.__answer_agent_type

    def get_rules_file_path(self) -> Path:
        return self.__rules_file_path

    def get_top_k(self) -> int:
        return self.__top_k

    def get_stopwords_file_path(self) -> Path:
        return self.__stopwords_file_path

    def get_top_n(self) -> int:
        return self.__top_n

    def get_chunk_path(self) -> Path:
        return self.__chunk_path

    def get_logs_dir_path(self) -> Path:
        return self.__logs_dir_path