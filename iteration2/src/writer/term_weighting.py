from typing import Dict, List, Tuple
from collections import Counter


class TermWeighting:
    
    def __init__(self, 
                 tf_weight: float = 1.0,
                 booster_weight: float = 2.0,
                 base_weight: float = 1.0):
        
        self.tf_weight = tf_weight
        self.booster_weight = booster_weight
        self.base_weight = base_weight
    #boosted_terms icerisinde olan terimlere ek ağırlık ver
    #terms icerisindeki terimlerin frekansına göre ağırlık ver
    def calculate_weights(self, 
                         terms: List[str], 
                         boosted_terms: List[str]) -> Dict[str, float]:
     
        weights: Dict[str, float] = {}
        
        # Terim frekansını hesapla
        term_frequency = Counter(terms)
        max_freq = max(term_frequency.values()) if term_frequency else 1
        
        # Her terim için ağırlık hesapla
        for term in term_frequency:
            term_lower = term.lower()
            
            # Temel ağırlık
            weight = self.base_weight
            
            # Terim frekansı ağırlığını ekle (normalizasyon ile)
            normalized_freq = term_frequency[term] / max_freq
            weight += (normalized_freq * self.tf_weight)
            
            # Eğer terim booster listesinde varsa, ek ağırlık ver
            if term_lower in [b.lower() for b in boosted_terms]:
                weight *= self.booster_weight
            
            weights[term] = weight
        
        return weights

    def rank_terms(self, 
                   terms: List[str], 
                   boosted_terms: List[str]) -> List[Tuple[str, float]]:
        
        weights = self.calculate_weights(terms, boosted_terms)
        
        # Ağırlığa göre azalan sırada sırala
        ranked = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        return ranked

    def get_top_terms(self, 
                      terms: List[str], 
                      boosted_terms: List[str],
                      top_k: int = 10) -> List[str]:
       
        ranked = self.rank_terms(terms, boosted_terms)
        return [term for term, _ in ranked[:top_k]]
    # Ağırlık istatistiklerini döndür
    def get_weight_stats(self, 
                        terms: List[str], 
                        boosted_terms: List[str]) -> Dict[str, any]:
       
        weights = self.calculate_weights(terms, boosted_terms)
        
        return {
            "total_terms": len(weights),
            "avg_weight": sum(weights.values()) / len(weights) if weights else 0,
            "max_weight": max(weights.values()) if weights else 0,
            "min_weight": min(weights.values()) if weights else 0
        }
