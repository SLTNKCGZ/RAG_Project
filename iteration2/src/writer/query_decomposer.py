from typing import List
import re


class QueryDecomposer:

    def __init__(self, conjunctions: List[str]):
        self.conjunctions = conjunctions

    def decompose(self, question: str) -> List[str]:
        if not question or question.strip() == "":
            return []

        question = question.strip()
        sub_queries = self._split_by_conjunctions(question)
        sub_queries = [q.strip() for q in sub_queries if q.strip()]

        if len(sub_queries) <= 1:
            return [question]
        return sub_queries

    def _split_by_conjunctions(self, question: str) -> List[str]:
        result = [question]
        for conjunction in self.conjunctions:
            new_result = []
            for q in result:
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
