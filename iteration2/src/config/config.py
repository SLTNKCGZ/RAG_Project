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
        retriever_alpha: float,
        retriever_beta: float,
        embedding_provider_type: str,
        stopwords_file_path: Path,
        suffixes_file_path: Path,
        conjunctions_file_path: Path,
        tf_weight: float,
        booster_weight: float,
        base_weight: float,
        top_n: int,
        proximity_window: int,
        proximity_bonus: int,
        title_boost: int,
        reranker_alpha: float,
        reranker_beta: float,
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
        self.__retriever_alpha = retriever_alpha
        self.__retriever_beta = retriever_beta
        self.__embedding_provider_type = embedding_provider_type
        self.__stopwords_file_path = stopwords_file_path
        self.__suffixes_file_path = suffixes_file_path
        self.__conjunctions_file_path = conjunctions_file_path
        self.__tf_weight = tf_weight
        self.__booster_weight = booster_weight
        self.__base_weight = base_weight
        self.__top_n = top_n
        self.__proximity_window = proximity_window
        self.__proximity_bonus = proximity_bonus
        self.__title_boost = title_boost
        self.__reranker_alpha = reranker_alpha
        self.__reranker_beta = reranker_beta
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

    def get_retriever_alpha(self) -> float:
        return self.__retriever_alpha

    def get_retriever_beta(self) -> float:
        return self.__retriever_beta

    def get_embedding_provider_type(self) -> str:
        return self.__embedding_provider_type

    def get_stopwords_file_path(self) -> Path:
        return self.__stopwords_file_path

    def get_suffixes_file_path(self) -> Path:
        return self.__suffixes_file_path

    def get_conjunctions_file_path(self) -> Path:
        return self.__conjunctions_file_path

    def get_tf_weight(self) -> float:
        return self.__tf_weight

    def get_booster_weight(self) -> float:
        return self.__booster_weight

    def get_base_weight(self) -> float:
        return self.__base_weight

    def get_top_n(self) -> int:
        return self.__top_n

    def get_proximity_window(self) -> int:
        return self.__proximity_window

    def get_proximity_bonus(self) -> int:
        return self.__proximity_bonus

    def get_title_boost(self) -> int:
        return self.__title_boost

    def get_reranker_alpha(self) -> float:
        return self.__reranker_alpha

    def get_reranker_beta(self) -> float:
        return self.__reranker_beta

    def get_chunk_path(self) -> Path:
        return self.__chunk_path

    def get_logs_dir_path(self) -> Path:
        return self.__logs_dir_path