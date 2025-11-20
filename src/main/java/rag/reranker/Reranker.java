package main.java.rag.reranker;
import java.util.List;
import rag.model.Hit;

public interface Reranker {
    /**
     * Gelen hit listesini puanlayıp yeniden sıralar.
     * @param query Original query terms
     * @param hits Elde edilen hits
     * @return Puanlanmış ve sıralanmış hit listesi
     */
    List<Hit> rerank(List<String> query, List<Hit> hits);
}
