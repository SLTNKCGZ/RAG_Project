package com.cse3063f25grp1.retrieval;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;

public class KeywordRetriever implements Retriever {

    private final int topK;

    public KeywordRetriever(int topK) {
        this.topK = topK;
    }

    @Override
    public List<Hit> retrieve(List<String> queryTerms, ChunkStore store) {
        if (queryTerms == null || queryTerms.isEmpty())
            return Collections.emptyList();

        Map<String, Hit> hitMap = new HashMap<>();

        for (Chunk chunk : store.getAllChunks()) {
            String chunkTextLower = safeLower(chunk.getText());
            int totalTf = 0;

            for (String term : queryTerms) {
                if (term == null || term.isEmpty())
                    continue;
                totalTf += countOccurrences(chunkTextLower, term.toLowerCase());
            }

            if (totalTf > 0) {
                String key = chunk.getDocId() + "||" + chunk.getChunkId();
                Hit h = hitMap.get(key);
                if (h == null) {
                    h = new Hit(chunk.getDocId(), chunk.getChunkId(), totalTf);
                    hitMap.put(key, h);
                } else {
                    h.setScore(h.getScore() + totalTf);
                }
            }
        }

        List<Hit> hits = new ArrayList<>(hitMap.values());
        hits.sort(Comparator
                .comparingInt(Hit::getScore).reversed()
                .thenComparing(Hit::getDocId)
                .thenComparing(Hit::getChunkId));

        if (hits.size() > topK) {
            return hits.subList(0, topK);
        } else {
            return hits;
        }
    }

    private static int countOccurrences(String haystackLower, String needleLower) {
        if (haystackLower == null || needleLower == null)
            return 0;
        int count = 0;
        int idx = haystackLower.indexOf(needleLower);
        while (idx != -1) {
            count++;
            idx = haystackLower.indexOf(needleLower, idx + needleLower.length());
        }
        return count;
    }

    private static String safeLower(String s) {
        return s == null ? "" : s.toLowerCase();
    }

}