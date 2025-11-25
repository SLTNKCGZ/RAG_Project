from pathlib import Path
from typing import Dict, List, Optional
import json

from src.model.chunk import Chunk


class ChunkStore:
    """
    In-memory store for chunks with efficient lookup.
    Uses composite key (docId||chunkId) for fast retrieval.
    """
    
    def __init__(self):
        """Initialize ChunkStore."""
        self.chunks: Dict[str, Chunk] = {}  # key: "docId||chunkId"
        self.document_titles: Dict[str, str] = {}  # key: docId
    
    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to the store."""
        key = f"{chunk.get_doc_id()}||{chunk.get_chunk_id()}"
        self.chunks[key] = chunk
    
    def get_chunk(self, doc_id: str, chunk_id: str) -> Optional[Chunk]:
        """Get a specific chunk by doc_id and chunk_id."""
        key = f"{doc_id}||{chunk_id}"
        return self.chunks.get(key)
    
    def get_all_chunks(self) -> List[Chunk]:
        """Get all chunks."""
        return list(self.chunks.values())
    
    def set_document_title(self, doc_id: str, title: str) -> None:
        """Set title for a document."""
        self.document_titles[doc_id] = title
    
    def get_document_title(self, doc_id: str) -> Optional[str]:
        """Get title for a document."""
        return self.document_titles.get(doc_id)
    
    def get_all_doc_ids(self) -> set:
        """Get all document IDs."""
        return set(self.document_titles.keys())
    
    def size(self) -> int:
        """Get total number of chunks."""
        return len(self.chunks)
    
    def __repr__(self) -> str:
        return f"ChunkStore(chunks={len(self.chunks)}, documents={len(self.document_titles)})"
