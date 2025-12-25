from typing import Dict, Any, Optional


class QueryCache:
   
    def __init__(self, max_size: int = 100):
       
        self.__cache: Dict[str, Any] = {}
        self.__max_size = max_size
    #query getir
    def get(self, query: str) -> Optional[Any]:
        
        return self.__cache.get(query.lower())

    def set(self, query: str, result: Any) -> None:
      
        query_lower = query.lower()
        
        # Önbellek sınırını kontrol et
        if len(self.__cache) >= self.__max_size:
            # En eski girdiye (FIFO) göre sil
            first_key = next(iter(self.__cache))
            del self.__cache[first_key]
        
        self.__cache[query_lower] = result
    
    #query var mı
    def has(self, query: str) -> bool:
      
        return query.lower() in self.__cache
    #önbelleği temizle
    def clear(self) -> None:
        
        self.__cache.clear()
    #on bellektei sorgu sayisini dondur
    def get_size(self) -> int:
       
        return len(self.__cache)

    def get_stats(self) -> Dict[str, int]:
        
        return {
            "cached_queries": len(self.__cache),
            "max_size": self.__max_size
        }
