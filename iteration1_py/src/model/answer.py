from typing import List


class Answer:
   
    def __init__(self, text: str = None, citations: List[str] = None):
       
        self.text = text
        self.citations = citations if citations is not None else []
    
    def get_text(self) -> str:
        return self.text
    
    def set_text(self, text: str) -> None:
        """Set the answer text."""
        self.text = text
    
    def get_citations(self) -> List[str]:
        return self.citations.copy()
    
    def add_citation(self, citation: str) -> None:
       
        if citation and citation.strip():
            self.citations.append(citation)
    
    def has_citations(self) -> bool:
        """Check if the answer has any citations."""
        return len(self.citations) > 0
    
    def to_single_line(self) -> str:
       
        result = self.text if self.text else ""
        
        if self.has_citations():
            result += " See: " + ", ".join(self.citations)
        
        return result
    
    def __str__(self) -> str:
        return self.to_single_line()
    
    def __repr__(self) -> str:
        return f"Answer(text={self.text!r}, citations={self.citations!r})"
