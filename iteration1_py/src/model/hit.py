class Hit:
   
    
    def __init__(self, doc_id: str = None, chunk_id: str = None, score: int = 0):
       
        self.doc_id = doc_id
        self.chunk_id = chunk_id
        self.score = score
    
    def get_doc_id(self) -> str:
        """Get the document ID."""
        return self.doc_id
    
    def get_chunk_id(self) -> str:
        """Get the chunk ID."""
        return self.chunk_id
    
    def get_score(self) -> int:
        """Get the relevance score."""
        return self.score
    
    def set_score(self, score: int) -> None:
       
        self.score = score
    
    def __str__(self) -> str:
        return f"Hit(doc_id={self.doc_id}, chunk_id={self.chunk_id}, score={self.score})"
    
    def __repr__(self) -> str:
        return f"Hit(doc_id={self.doc_id!r}, chunk_id={self.chunk_id!r}, score={self.score})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Hit):
            return False
        return (self.doc_id == other.doc_id and 
                self.chunk_id == other.chunk_id and 
                self.score == other.score)
    
    def __hash__(self) -> int:

        
        return hash((self.doc_id, self.chunk_id, self.score))
