from typing import Dict, List, Set, Optional
from src.model.chunk import Chunk

class ChunkStore:
    
    def __init__(self) -> None:
        self.__chunks: Dict[str, Chunk] = {}  # key: "docId||chunkId"
        self.__document_titles: Dict[str, str] = {}  # key: docId, value: title

    def add_chunk(self, chunk: Chunk) -> None:
        key = f"{chunk.get_doc_id()}||{chunk.get_chunk_id()}"
        self.__chunks[key] = chunk

    def get_chunk(self, doc_id: str, chunk_id: str) -> Optional[Chunk]:
        key = f"{doc_id}||{chunk_id}"
        return self.__chunks.get(key)

    def get_all_chunks(self) -> List[Chunk]:
        return list(self.__chunks.values())

    def set_document_title(self, doc_id: str, title: str) -> None:
        self.__document_titles[doc_id] = title

    def get_document_title(self, doc_id: str) -> Optional[str]:
        return self.__document_titles.get(doc_id)

    def get_all_doc_ids(self) -> Set[str]:
        return set(self.__document_titles.keys())

    def size(self) -> int:
        return len(self.__chunks)
