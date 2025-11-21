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
        // Using real CSE data: research assistant info with different frequencies
        store.addChunk(new Chunk("arastirma_gorevlileri.txt", "serap_korkmaz",
                "Arş. Gör. Serap Korkmaz Bilgisayar Mühendisliği Marmara Üniversitesi", "arastirma_gorevlileri", 0, 70)); // 2 match
        store.addChunk(new Chunk("arastirma_gorevlileri.txt", "zuhal_ozturk",
                "Arş. Gör. Zuhal Öztürk Bilgisayar Mühendisliği", "arastirma_gorevlileri", 71, 120)); // 1 match
        store.addChunk(new Chunk("basari.txt", "yarismalar",
                "Fakülte öğrenci yarışmaları başarıları", "basari_bilgileri", 0, 40)); // 0 match

        KeywordRetriever retriever = new KeywordRetriever(2);

        List<Hit> hits = retriever.retrieve(Arrays.asList("bilgisayar", "mühendisliği"), store);

        // Highest score: serap_korkmaz (2 matches), then zuhal_ozturk (1 match); topK=2
        assertEquals(2, hits.size());
        assertEquals("arastirma_gorevlileri.txt", hits.get(0).getDocId());
        assertEquals("serap_korkmaz", hits.get(0).getChunkId());
        assertEquals("arastirma_gorevlileri.txt", hits.get(1).getDocId());
        assertEquals("zuhal_ozturk", hits.get(1).getChunkId());
    }

    @Test
    void handlesEmptyOrNullQueriesGracefully() {
        ChunkStore store = new ChunkStore();
        store.addChunk(new Chunk("test.txt", "chunk1", "test content", "section", 0, 20));

        KeywordRetriever retriever = new KeywordRetriever(10);

        // Empty query list
        List<Hit> hits1 = retriever.retrieve(List.of(), store);
        assertEquals(0, hits1.size());

        // Null query
        List<Hit> hits2 = retriever.retrieve(null, store);
        assertEquals(0, hits2.size());
    }
}


