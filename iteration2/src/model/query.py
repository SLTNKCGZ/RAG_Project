class Query:
    def __init__(self, text: str = None):
        self.__text = text

    # Getter
    def get_text(self) -> str:
        return self.__text

    # String representation
    def __str__(self) -> str:
        return f"Query{{text='{self.__text}'}}"
    
