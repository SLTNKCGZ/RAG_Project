package com.cse3063f25grp1.answer;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Hit;

import java.util.List;

/**
 * Strategy interface for answer generation
 * SOLID: DIP - Depend on abstraction
 * Design Pattern: Strategy
 */
public interface AnswerAgent {
    /**
     * Generate answer from top hits
     * 
     * @param query      The query terms
     * @param topHits    The top retrieved and reranked hits
     * @param chunkStore The chunk store for reference
     * @return Answer with text and citations
     */
    Answer answer(List<String> query, List<Hit> topHits, ChunkStore chunkStore);
}
