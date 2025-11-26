from typing import List

class Answer:
    
    def __init__(self, text: str, citations: List[str]):
        self.__text: str = text
        self.__citations: List[str] = list(citations)

    def get_text(self) -> str:
        return self.__text
    
    def set_text(self, text: str) -> None:
        self.__text = text
    
    def get_citations(self) -> List[str]:
        return self.__citations.copy()
    
    def add_citation(self, citation: str) -> None:
        if citation and citation.strip():
            self.__citations.append(citation)

    def has_citations(self) -> bool:
        return bool(self.__citations)
    
    def to_single_line(self) -> str:
        current_text = self.__text if self.__text else ""
        
        if self.has_citations():
            citation_string = ", ".join(self.__citations)
            return f"{current_text} See: {citation_string}"
        
        return current_text
    
    def __str__(self) -> str:
        return self.to_single_line()

