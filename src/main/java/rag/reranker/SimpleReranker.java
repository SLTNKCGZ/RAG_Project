package main.java.rag.reranker;

import main.java.rag.data.ChunkStore;
import main.java.rag.model.Chunk;
import main.java.rag.model.Hit;

import java.util.*;

public class SimpleReranker implements Reranker {

    private final int proximityWindow; // karakter
    private final int proximityBonus;
    private final int titleBoost;

    // Constructor zorunlu, default yok
    public SimpleReranker(int proximityWindow, int proximityBonus, int titleBoost) {
        this.proximityWindow = proximityWindow;
        this.proximityBonus = proximityBonus;
        this.titleBoost = titleBoost;
    }

    @Override
    public List<Hit> rerank(List<String> queryTerms, List<Hit> hits, ChunkStore store) {
        if (hits == null || hits.isEmpty()) return Collections.emptyList();
        List<Hit> reranked = new ArrayList<>();

        for (Hit hit : hits) {
            Chunk chunk = store.getChunk(hit.getDocId(), hit.getChunkId());
            if (chunk == null) continue;

            int score = hit.getScore() * 10; // tf_sum * 10

            // proximity bonus: herhangi iki terim proximityWindow içinde ise ekle
            if (queryTerms != null && queryTerms.size() >= 2) {
                if (anyTermsWithinWindow(chunk.getText().toLowerCase(), queryTerms, proximityWindow)) {
                    score += proximityBonus;
                }
            }

            // title boost: doc title veya section title herhangi bir query terimi içeriyorsa
            String docTitle = store.getDocumentTitle(hit.getDocId());
            if (docTitle != null) {
                String titleLower = docTitle.toLowerCase();
                for (String term : queryTerms) {
                    if (term == null) continue;
                    if (titleLower.contains(term.toLowerCase())) {
                        score += titleBoost;
                        break;
                    }
                }
            }

            reranked.add(new Hit(hit.getDocId(), hit.getChunkId(), score));
        }

        // stable sort: score desc, docId asc, chunkId asc
        reranked.sort(Comparator
                .comparingInt(Hit::getScore).reversed()
                .thenComparing(Hit::getDocId)
                .thenComparing(Hit::getChunkId));

        return reranked;
    }

    // helper: herhangi iki terim proximityWindow içinde mi
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