package com.cse3063f25grp1.retrieval;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class KeywordRetrieverTest {

    @Test
    void ranksByTotalTermFrequencyAndAppliesTopK() {
        ChunkStore store = new ChunkStore();
        store.addChunk(new Chunk("doc1", "c1", "kayıt kayıt kayıt", "s1", 0, 20)); // 3 match
        store.addChunk(new Chunk("doc2", "c1", "kayıt ve danışman", "s1", 0, 20)); // 1 match
        store.addChunk(new Chunk("doc3", "c1", "hiç alakalı değil", "s1", 0, 20)); // 0

        KeywordRetriever retriever = new KeywordRetriever(2);

        List<Hit> hits = retriever.retrieve(List.of("kayıt"), store);

        // En yüksek skor doc1, sonra doc2; topK=2 olduğu için 2 sonuç
        assertEquals(2, hits.size());
        assertEquals("doc1", hits.get(0).getDocId());
        assertEquals("doc2", hits.get(1).getDocId());
    }

    @Test
    void tiesAreBrokenByDocIdThenChunkId() {
        ChunkStore store = new ChunkStore();
        // her biri 1 kez "kayıt" içeriyor => skor eşit; sıralama docId, sonra chunkId'ye göre
        store.addChunk(new Chunk("docB", "c1", "kayıt işlemi", "s1", 0, 20));
        store.addChunk(new Chunk("docA", "c2", "kayıt işlemi", "s1", 0, 20));

        KeywordRetriever retriever = new KeywordRetriever(10);

        List<Hit> hits = retriever.retrieve(Arrays.asList("kayıt"), store);

        assertEquals(2, hits.size());
        assertEquals("docA", hits.get(0).getDocId());
        assertEquals("docB", hits.get(1).getDocId());
    }
}


