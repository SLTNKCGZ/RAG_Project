package main.java.rag.retrieval;

import java.util.List;
import main.java.rag.data.ChunkStore;
import main.java.rag.model.Hit;


public interface Retriever {
    
    List<Hit> retrieve(List<String> queryTerms, ChunkStore store);
}
