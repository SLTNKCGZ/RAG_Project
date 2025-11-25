from typing import List


class Chunk:
   
    def __init__(self, doc_id: str = None, chunk_id: str = None, text: str = None, 
                 section_id: str = None, start_offset: int = None, end_offset: int = None):
       
        self.doc_id = doc_id
        self.chunk_id = chunk_id
        self.text = text
        self.section_id = section_id
        self.start_offset = start_offset if start_offset is not None else 0
        self.end_offset = end_offset if end_offset is not None else 0
    
    def get_doc_id(self) -> str:
        """Get the document ID."""
        return self.doc_id
    
    def get_chunk_id(self) -> str:
        """Get the chunk ID."""
        return self.chunk_id
    
    def get_text(self) -> str:
        """Get the chunk text."""
        return self.text
    
    def get_section_id(self) -> str:
        """Get the section ID."""
        return self.section_id
    
    def get_start_offset(self) -> int:
        """Get the start offset."""
        return self.start_offset
    
    def get_end_offset(self) -> int:
        """Get the end offset."""
        return self.end_offset
    
    def get_sentences(self) -> List[str]:
      

        if not self.text:
            return []
        
        # Simple sentence splitting by common delimiters
        sentences = []
        current = ""
        
        for char in self.text:
            current += char
            if char in '.!?':
                sentences.append(current.strip())
                current = ""
        
        if current.strip():
            sentences.append(current.strip())
        
        return sentences
    
    def get_length(self) -> int:
        
        return len(self.text) if self.text else 0
    
    def __str__(self) -> str:
        return f"Chunk(doc_id={self.doc_id}, chunk_id={self.chunk_id}, text_length={self.get_length()})"
    
    def __repr__(self) -> str:
        return f"Chunk(doc_id={self.doc_id!r}, chunk_id={self.chunk_id!r}, text={self.text!r}, section_id={self.section_id!r}, start_offset={self.start_offset}, end_offset={self.end_offset})"
