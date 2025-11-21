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
    void appliesProximityBonusForCloseTerms() {
        ChunkStore store = new ChunkStore();
        // Text from research assistants file: terms "arş" and "gör" are close together
        Chunk chunk = new Chunk("arastirma_gorevlileri.txt", "serap_korkmaz",
                "Arş. Gör. Serap Korkmaz PhD: Bilgisayar Müh. - Marmara Üniversitesi. Ofis: M2-201",
                "arastirma_gorevlileri", 0, 80);
        store.addChunk(chunk);
        store.setDocumentTitle("arastirma_gorevlileri.txt", "Araştırma Görevlileri");

        Hit baseHit = new Hit("arastirma_gorevlileri.txt", "serap_korkmaz", 3); // tf_sum=3

        // window=50, proximityBonus=5, titleBoost=3
        SimpleReranker reranker = new SimpleReranker(50, 5, 3);

        List<Hit> reranked = reranker.rerank(
                Arrays.asList("arş", "gör"),
                List.of(baseHit),
                store);

        // base score: 3*10=30, +5 proximity (Arş. Gör. are close), +3 title = 38
        assertEquals(1, reranked.size());
        assertEquals(38, reranked.get(0).getScore());
    }

    @Test
    void appliesTitleBoostForRelevantTitles() {
        ChunkStore store = new ChunkStore();
        // Text from success file: title contains "öğrenci" term
        Chunk chunk = new Chunk("basari.txt", "yarismalar",
                "Son 3 senede 30 öğrencimiz 12 farklı yarışmada ödül almışlardır.",
                "basari_bilgileri", 0, 65);
        store.addChunk(chunk);
        store.setDocumentTitle("basari.txt", "Öğrenci Başarıları");

        Hit baseHit = new Hit("basari.txt", "yarismalar", 2); // tf_sum=2

        // window=50, proximityBonus=5, titleBoost=3
        SimpleReranker reranker = new SimpleReranker(50, 5, 3);

        List<Hit> reranked = reranker.rerank(
                Arrays.asList("öğrenci", "yarışma"),
                List.of(baseHit),
                store);

        // base score: 2*10=20, +5 proximity (öğrenci and yarışma are within window), +3 title = 28
        assertEquals(1, reranked.size());
        assertEquals(28, reranked.get(0).getScore());
    }
}


