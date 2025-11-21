package com.cse3063f25grp1.reranker;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SimpleRerankerTest {

    @Test
    void appliesProximityBonusAndTitleBoost() {
        ChunkStore store = new ChunkStore();
        // Text: iki terim birbirine yakın
        Chunk chunk = new Chunk("doc1", "c1",
                "kayıt formu hemen burada. kayıt işlemi adımları.",
                "sec1", 0, 60);
        store.addChunk(chunk);
        store.setDocumentTitle("doc1", "Öğrenci kayıt kılavuzu");

        Hit baseHit = new Hit("doc1", "c1", 2); // tf_sum=2

        // window=50, proximityBonus=5, titleBoost=3
        SimpleReranker reranker = new SimpleReranker(50, 5, 3);

        List<Hit> reranked = reranker.rerank(
                Arrays.asList("kayıt", "formu"),
                List.of(baseHit),
                store);

        // base score: 2*10=20, +5 proximity, +3 title = 28
        assertEquals(1, reranked.size());
        assertEquals(28, reranked.get(0).getScore());
    }

    @Test
    void returnsEmptyListWhenNoHits() {
        ChunkStore store = new ChunkStore();
        SimpleReranker reranker = new SimpleReranker(10, 5, 3);

        List<Hit> reranked = reranker.rerank(List.of("kayıt"), List.of(), store);

        assertEquals(0, reranked.size());
    }
}


