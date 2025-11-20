package main.java.rag.retrieval;

import java.util.List;
import rag.model.Hit;

public interface Retriever {
    /**
     * Verilen terimler ile index veya chunk listesinde arama yapar.
     * @param terms Aranacak anahtar kelimeler
     * @return Eşleşen Hit listesi
     */
    List<Hit> retrieve(List<String> terms);
}
