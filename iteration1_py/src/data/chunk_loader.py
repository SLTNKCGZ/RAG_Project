import json
from pathlib import Path
from typing import Optional

from src.model.chunk import Chunk
from src.data.chunk_store import ChunkStore


class ChunkLoader:
   
    def load_chunks(self, chunks_json_path: Path) -> ChunkStore:
       
        chunks_json_path = Path(chunks_json_path)
        
        if not chunks_json_path.exists():
            raise FileNotFoundError(f"Chunks file not found: {chunks_json_path}")
        
        try:
            with open(chunks_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            chunk_store = ChunkStore()
            self._parse_and_load_chunks(data, chunk_store)
            
            return chunk_store
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {chunks_json_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load chunks from {chunks_json_path}: {e}")
    
    @staticmethod
    def _parse_and_load_chunks(data: dict, chunk_store: ChunkStore) -> None:
       
        if 'documents' not in data:
            raise ValueError("Invalid JSON structure: 'documents' key not found")
        
        documents = data['documents']
        
        for document in documents:
            ChunkLoader._parse_document(document, chunk_store)
    
    @staticmethod
    def _parse_document(doc_data: dict, chunk_store: ChunkStore) -> None:
        
        doc_id = doc_data.get('docId')
        if doc_id is None:
            raise ValueError("Invalid document: docId not found")
        
        title = doc_data.get('title')
        if title:
            chunk_store.set_document_title(doc_id, title)
        
        sections = doc_data.get('sections', [])
        for section in sections:
            ChunkLoader._parse_section(section, doc_id, chunk_store)
    
    @staticmethod
    def _parse_section(section_data: dict, doc_id: str, chunk_store: ChunkStore) -> None:
       
        section_id = section_data.get('sectionId', '')
        chunks = section_data.get('chunks', [])
        
        for chunk_data in chunks:
            ChunkLoader._parse_chunk(chunk_data, doc_id, section_id, chunk_store)
    
    @staticmethod
    def _parse_chunk(chunk_data: dict, doc_id: str, section_id: str, chunk_store: ChunkStore) -> None:
        
        chunk_id = chunk_data.get('chunkId')
        content = chunk_data.get('content')
        
        if not chunk_id or not content:
            raise ValueError("Invalid chunk: missing required fields (chunkId, content)")
        
        start_offset = chunk_data.get('startOffset', 0)
        end_offset = chunk_data.get('endOffset', 0)
        
        chunk = Chunk(
            doc_id=doc_id,
            chunk_id=chunk_id,
            text=content,
            section_id=section_id,
            start_offset=start_offset,
            end_offset=end_offset
        )
        
        chunk_store.add_chunk(chunk)
