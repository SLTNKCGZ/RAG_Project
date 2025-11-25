class Query:
    
    
    def __init__(self, text: str = None):
      
        self.text = text
    
    def get_text(self) -> str:
        
        return self.text
    
    def set_text(self, text: str) -> None:
        
        self.text = text
    
    def __str__(self) -> str:
        return f"Query(text={self.text!r})"
    
    def __repr__(self) -> str:
        return f"Query(text={self.text!r})"
