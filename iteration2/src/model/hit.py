class Hit:
    def __init__(self, doc_id: str = None, chunk_id: str = None, score: int = 0):
        self.__doc_id = doc_id
        self.__chunk_id = chunk_id
        self.__score = score

    # Getters
    def get_doc_id(self) -> str:
        return self.__doc_id

    def get_chunk_id(self) -> str:
        return self.__chunk_id

    def get_score(self) -> int:
        return self.__score

    # Setter
    def set_score(self, score: int) -> None:
        self.__score = score

    # String representation
    def __str__(self) -> str:
        return f"Hit{{docId='{self.__doc_id}', chunkId='{self.__chunk_id}', score={self.__score}}}"
