package main.java.rag.answer;

import main.java.rag.data.ChunkStore;
import main.java.rag.model.Answer;
import main.java.rag.model.Hit;

import java.util.List;

/**
 * Strategy interface for answer generation
 * SOLID: DIP - Depend on abstraction
 * Design Pattern: Strategy
 */
public interface AnswerAgent {
    /**
     * Generate answer from top hits
     * @param query The query terms
     * @param topHits The top retrieved and reranked hits
     * @param chunkStore The chunk store for reference
     * @return Answer with text and citations
     */
    Answer answer(List<String> query, List<Hit> topHits, ChunkStore chunkStore);
}
