from typing import List, Optional
import re
from src.embedding.embedding_provider import EmbeddingProvider
from src.writer.simple_stemmer import SimpleStemmer


class SimpleEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic stub embedding provider.
    Same text -> same vector always.
    Uses word-based embedding with TF-like weighting for better semantic similarity.
    """

    def __init__(self, stemmer: Optional[SimpleStemmer] = None):
        self.__stemmer = stemmer

    def __word_hash(self, word: str) -> int:
        hash_val = 0
        for char in word:
            hash_val = ((hash_val * 31) + ord(char)) & 0x7FFFFFFF
        return hash_val

    def embed(self, text: str) -> List[float]:
        vector = [0.0] * 128
        if not text:
            return vector

        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return vector

        word_counts = {}
        for word in words:
            if self.__stemmer:
                word = self.__stemmer.stem(word)
            if len(word) < 2:
                continue
            word_counts[word] = word_counts.get(word, 0) + 1

        total_words = sum(word_counts.values())
        if total_words == 0:
            return vector

        for word, count in word_counts.items():
            word_hash = self.__word_hash(word)
            tf = count / total_words
            for i in range(4):
                idx = (word_hash + i * 37) % 128
                vector[idx] += tf

        return vector