from typing import List
import re

class Chunk:
   
    def __init__(self, doc_id: str = None, chunk_id: str = None, text: str = None, 
                 section_id: str = None, start_offset: int = 0, end_offset: int = 0):
       
        self.__doc_id = doc_id
        self.__chunk_id = chunk_id
        self.__text = text
        self.__section_id = section_id
        self.__start_offset = start_offset if start_offset is not None else 0
        self.__end_offset = end_offset if end_offset is not None else 0
    
    def get_doc_id(self) -> str:
        """Get the document ID."""
        return self.__doc_id
    
    def get_chunk_id(self) -> str:
        """Get the chunk ID."""
        return self.__chunk_id
    
    def get_text(self) -> str:
        """Get the chunk text."""
        return self.__text
    
    def get_section_id(self) -> str:
        """Get the section ID."""
        return self.__section_id
    
    def get_start_offset(self) -> int:
        """Get the start offset."""
        return self.__start_offset
    
    def get_end_offset(self) -> int:
        """Get the end offset."""
        return self.__end_offset
    
    def get_sentences(self) -> List[str]:
        sentences = []
        if not self.__text:
            return sentences

        parts = re.split(r'(?<=[.!?])\s+', self.__text)
        for part in parts:
            trimmed = part.strip()
            if trimmed:
                sentences.append(trimmed)

        if not sentences and self.__text.strip():
            sentences.append(self.__text.strip())

        return sentences
    
    def contains(self, term: str) -> bool:
        if not self.__text or not term:
            return False
        return term.lower() in self.__text.lower()
    
    def format_citation(self) -> str:
        return f"{self.__doc_id}:{self.__section_id}:{self.__start_offset}-{self.__end_offset}"
    
    def __str__(self):
        text_length = len(self.__text) if self.__text else 0
        return (
            f"Chunk{{docId='{self.__doc_id}', chunkId='{self.__chunk_id}', "
            f"sectionId='{self.__section_id}', startOffset={self.__start_offset}, "
            f"endOffset={self.__end_offset}, textLength={text_length}}}"
        )
