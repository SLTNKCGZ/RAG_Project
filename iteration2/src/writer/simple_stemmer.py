from typing import List, Dict


class SimpleStemmer:
    
    # Türkçe suffixler (ekler) - uzundan kısaya sıralı
    SUFFIXES = [
        # 4+ karakterli suffixler
        "-ımızda", "-inızda", "-larında", "-lerinde",
        "-ılarında", "-ilerinde", "-sından", "-sinden",
        
        # 3 karakterli suffixler
        "-lar", "-ler", "-da", "-de", "-ta", "-te",
        "-ımız", "-inız", "-ları", "-leri", "-sız",
        "-ine", "-ına", "-ında", "-inde", "-ında", "-inde",
        "-dan", "-den", "-tan", "-ten",
        
        # 2 karakterli suffixler
        "-im", "-in", "-ı", "-i", "-um", "-ün",
        "-ım", "-ım", "-um", "-um",
        "-la", "-le",
        "-ca", "-ce",
    ]

    def __init__(self, min_word_length: int = 3):
       
        self.min_word_length = min_word_length
        # Suffixleri uzundan kısaya sırayla düzenle
        self.suffixes_sorted = sorted(self.SUFFIXES, key=len, reverse=True)

    def stem(self, word: str) -> str:
        
        if not word or len(word) < self.min_word_length:
            return word

        word_lower = word.lower()
        stemmed = word_lower

        # Her suffix'i kontrol et ve kaldır (uzundan kısaya)
        for suffix in self.suffixes_sorted:
            if stemmed.endswith(suffix):
                # Suffix'i kaldır ve sonuç minimum uzunluk kontrolü yap
                root = stemmed[:-len(suffix)]
                if len(root) >= 2:  # Kök en az 2 karakterli olmalı
                    stemmed = root
                    break  # İlk matching suffix'i kaldır ve dur

        return stemmed

    def stem_terms(self, terms: List[str]) -> List[str]:
        
        stemmed_terms = []
        for term in terms:
            stemmed_term = self.stem(term)
            stemmed_terms.append(stemmed_term)
        return stemmed_terms

    def stem_with_mapping(self, terms: List[str]) -> Dict[str, str]:
        
        mapping = {}
        for term in terms:
            stemmed = self.stem(term)
            mapping[term] = stemmed
        return mapping

    def get_unique_stems(self, terms: List[str]) -> List[str]:
       
        stemmed_terms = self.stem_terms(terms)
        # Sıra koruyarak benzersizleri al (dict ile)
        unique_stems = list(dict.fromkeys(stemmed_terms))
        return unique_stems

    def compare_terms(self, term1: str, term2: str) -> bool:
        
        return self.stem(term1) == self.stem(term2)

    def get_stats(self, terms: List[str]) -> Dict[str, int]:
       
        mapping = self.stem_with_mapping(terms)
        unique_before = len(set(terms))
        unique_after = len(set(mapping.values()))
        
        return {
            "total_terms": len(terms),
            "unique_before_stemming": unique_before,
            "unique_after_stemming": unique_after,
            "duplicates_eliminated": unique_before - unique_after
        }
