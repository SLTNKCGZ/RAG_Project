package main.java.rag.reranker;
import java.util.List;
import main.java.rag.data.ChunkStore;
import main.java.rag.model.Hit;


public interface Reranker {
    List<Hit> rerank(List<String> query, List<Hit> hits,ChunkStore store);
}
