package main.java.rag.reranker;

import main.java.rag.data.ChunkStore;
import main.java.rag.model.Chunk;
import main.java.rag.model.Hit;

import java.util.*;

public class SimpleReranker implements Reranker {

    private final int proximityWindow;  // karakter
    private final int proximityBonus;

    public SimpleReranker() {
        this.proximityWindow = 15;
        this.proximityBonus = 5;
    }

    public SimpleReranker(int proximityWindow, int proximityBonus) {
        this.proximityWindow = proximityWindow;
        this.proximityBonus = proximityBonus;
    }

    @Override
    public List<Hit> rerank(List<String> queryTerms, List<Hit> hits, ChunkStore store) {
        if (hits == null || hits.isEmpty()) return Collections.emptyList();
        List<Hit> reranked = new ArrayList<>();

        for (Hit hit : hits) {
            Chunk chunk = store.getChunk(hit.getDocId(), hit.getChunkId());
            if (chunk == null) continue;

            int score = hit.getScore();
            if (queryTerms != null && queryTerms.size() >= 2) {
                if (anyTermsWithinWindow(chunk.getText().toLowerCase(), queryTerms, proximityWindow)) {
                    score += proximityBonus;
                }
            }

            reranked.add(new Hit(hit.getDocId(), hit.getChunkId(), score));
        }

        reranked.sort(Comparator
                .comparingInt(Hit::getScore).reversed()
                .thenComparing(Hit::getDocId)
                .thenComparing(Hit::getChunkId));

        return reranked;
    }

    private boolean anyTermsWithinWindow(String text, List<String> terms, int window) {
        List<Integer> positions = new ArrayList<>();
        for (String term : terms) {
            if (term == null || term.isEmpty()) continue;
            String t = term.toLowerCase();
            int idx = text.indexOf(t);
            while (idx != -1) {
                positions.add(idx);
                idx = text.indexOf(t, idx + 1);
            }
        }
        if (positions.size() < 2) return false;
        Collections.sort(positions);
        for (int i = 1; i < positions.size(); i++) {
            if (positions.get(i) - positions.get(i - 1) <= window) return true;
        }
        return false;
    }
}