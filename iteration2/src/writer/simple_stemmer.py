from typing import List, Optional


class SimpleStemmer:

    def __init__(self, suffixes: List[str], min_word_length: int = 3):
        self.min_word_length = min_word_length
        self.suffixes_sorted = sorted(suffixes, key=len, reverse=True)

    def stem(self, word: str) -> str:
        if not word or len(word) < self.min_word_length:
            return word

        word_lower = word.lower()
        stemmed = word_lower

        for suffix in self.suffixes_sorted:
            if stemmed.endswith(suffix):
                root = stemmed[:-len(suffix)]
                if len(root) >= 2:
                    stemmed = root
                    break

        return stemmed

    def stem_terms(self, terms: List[str]) -> List[str]:
        return [self.stem(term) for term in terms]
