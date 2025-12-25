from typing import List
import re


class QueryDecomposer:
   

    def __init__(self):
       
        # Sorguyu bölemek için kullanılan anahtar bağlaçlar
        self.conjunctions = ["ve", "or", "ya da", "veya", "ile ilgili", ",", "veyahut", "hem de"]

    def decompose(self, question: str) -> List[str]:
      
        if not question or question.strip() == "":
            return []

        # Sorguyu temizle
        question = question.strip()

        # Eğer sorgu birden fazla bağlaç içeriyorsa böl
        sub_queries = self._split_by_conjunctions(question)

        # Boş sorguları kaldır
        sub_queries = [q.strip() for q in sub_queries if q.strip()]

        if len(sub_queries) == 0:
            return [question]
        elif len(sub_queries) == 1:
            return [question]
        else:
            return sub_queries

    def _split_by_conjunctions(self, question: str) -> List[str]:
       
        result = [question]

        for conjunction in self.conjunctions:
            new_result = []
            for q in result:
                # Case-insensitive split
                parts = re.split(rf'\s+{re.escape(conjunction)}\s+', q, flags=re.IGNORECASE)
                new_result.extend(parts)
            result = new_result

        return result

    def is_complex_query(self, question: str) -> bool:
        
        if not question or question.strip() == "":
            return False

        for conjunction in self.conjunctions:
            if re.search(rf'\s+{re.escape(conjunction)}\s+', question, flags=re.IGNORECASE):
                return True

        return False
