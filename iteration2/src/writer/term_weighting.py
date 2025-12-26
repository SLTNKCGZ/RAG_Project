from typing import Dict, List, Tuple
from collections import Counter


class TermWeighting:

    def __init__(self, tf_weight: float = 1.0, booster_weight: float = 2.0, base_weight: float = 1.0):
        self.tf_weight = tf_weight
        self.booster_weight = booster_weight
        self.base_weight = base_weight

    def calculate_weights(self, terms: List[str], boosted_terms: List[str]) -> Dict[str, float]:
        weights: Dict[str, float] = {}
        term_frequency = Counter(terms)
        max_freq = max(term_frequency.values()) if term_frequency else 1

        for term in term_frequency:
            term_lower = term.lower()
            weight = self.base_weight
            normalized_freq = term_frequency[term] / max_freq
            weight += (normalized_freq * self.tf_weight)

            if term_lower in [b.lower() for b in boosted_terms]:
                weight *= self.booster_weight

            weights[term] = weight

        return weights

    def rank_terms(self, terms: List[str], boosted_terms: List[str]) -> List[Tuple[str, float]]:
        weights = self.calculate_weights(terms, boosted_terms)
        return sorted(weights.items(), key=lambda x: x[1], reverse=True)
