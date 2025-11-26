import json
from pathlib import Path
from src.data.chunk_store import ChunkStore
from src.model.chunk import Chunk

class ChunkLoader:
    

    def load_chunks(self, chunks_json_path: Path) -> ChunkStore:
        try:
            with open(chunks_json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            chunk_store = ChunkStore()
            self.__parse_json_and_load_chunks(json_content, chunk_store)
            return chunk_store

        except Exception as e:
            raise RuntimeError(f"Failed to load chunks from: {chunks_json_path}") from e

    def __parse_json_and_load_chunks(self, json_content: dict, chunk_store: ChunkStore) -> None:
        documents = json_content.get("documents", [])
        for doc in documents:
            self.__parse_document(doc, chunk_store)

    def __parse_document(self, doc: dict, chunk_store: ChunkStore) -> None:
        doc_id = doc.get("docId")
        if doc_id is None:
            raise RuntimeError("Invalid document: docId not found")

        title = doc.get("title")
        if title:
            chunk_store.set_document_title(doc_id, title)

        sections = doc.get("sections", [])
        for section in sections:
            self.__parse_section(section, doc_id, chunk_store)

    def __parse_section(self, section: dict, doc_id: str, chunk_store: ChunkStore) -> None:
        section_id = section.get("sectionId", "")
        chunks = section.get("chunks", [])
        for chunk in chunks:
            self.__parse_chunk(chunk, doc_id, section_id, chunk_store)

    def __parse_chunk(self, chunk: dict, doc_id: str, section_id: str, chunk_store: ChunkStore) -> None:
        chunk_id = chunk.get("chunkId")
        content = chunk.get("content")
        start_offset = chunk.get("startOffset", 0)
        end_offset = chunk.get("endOffset", 0)

        if chunk_id is None or content is None:
            raise RuntimeError("Invalid chunk: missing required fields")

        chunk_obj = Chunk(
            doc_id=doc_id,
            chunk_id=chunk_id,
            text=content,
            section_id=section_id,
            start_offset=start_offset,
            end_offset=end_offset
        )
        chunk_store.add_chunk(chunk_obj)
