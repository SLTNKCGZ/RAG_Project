package main.java.rag.retrieval;

import main.java.rag.data.ChunkStore;
import main.java.rag.model.Chunk;
import main.java.rag.model.Hit;

import java.util.*;

public class KeywordRetriever implements Retriever {

    private final int defaultTopK;

    public KeywordRetriever() {
        this.defaultTopK = 10;
    }

    public KeywordRetriever(int topK) {
        this.defaultTopK = topK;
    }

    @Override
    public List<Hit> retrieve(List<String> queryTerms, ChunkStore store, int topK) {
        if (queryTerms == null || queryTerms.isEmpty()) return Collections.emptyList();
        int k = topK > 0 ? topK : defaultTopK;

        Map<String, Hit> hitMap = new HashMap<>();

        for (Chunk chunk : store.getAllChunks()) {
            String textLower = chunk.getText() == null ? "" : chunk.getText().toLowerCase();
            int tfSum = 0;

            for (String term : queryTerms) {
                if (term == null || term.isEmpty()) continue;
                tfSum += countOccurrences(textLower, term.toLowerCase());
            }

            if (tfSum > 0) {
                String key = chunk.getDocId() + "||" + chunk.getChunkId();
                hitMap.put(key, new Hit(chunk.getDocId(), chunk.getChunkId(), tfSum));
            }
        }

        List<Hit> hits = new ArrayList<>(hitMap.values());
        hits.sort(Comparator
                .comparingInt(Hit::getScore).reversed()
                .thenComparing(Hit::getDocId)
                .thenComparing(Hit::getChunkId));

        return k > 0 && hits.size() > k ? hits.subList(0, k) : hits;
    }

    private int countOccurrences(String text, String term) {
        int count = 0;
        int idx = text.indexOf(term);
        while (idx != -1) {
            count++;
            idx = text.indexOf(term, idx + term.length());
        }
        return count;
    }
}