package com.cse3063f25grp1.answer;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;

class TemplateAnswerAgentTest {

    @Test
    void selectsSentenceThatContainsAllQueryTerms() {
        ChunkStore store = new ChunkStore();
        String text = "Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir. E-posta adresi haydar.ozer@marmara.edu.tr'dir. " +
                "Erasmus başvuruları bölüm koordinatörü üzerinden yapılır.";
        Chunk chunk = new Chunk("erasmus.txt", "koordinator", text, "erasmus_bilgileri", 0, text.length());
        store.addChunk(chunk);
        store.setDocumentTitle("erasmus.txt", "Erasmus Bilgileri");

        Hit hit = new Hit("erasmus.txt", "koordinator", 5);

        TemplateAnswerAgent agent = new TemplateAnswerAgent();
        Answer answer = agent.answer(
                List.of("erasmus", "koordinatörü"),
                List.of(hit),
                store);

        String answerText = answer.getText();

        assertTrue(answerText.startsWith("Bu cevap \"Erasmus Bilgileri\" başlıklı belgenin erasmus_bilgileri bölümünden alınmıştır."));
        assertTrue(answerText.toLowerCase().contains("erasmus"));
        assertTrue(answerText.toLowerCase().contains("koordinatörü"));
    }

    @Test
    void formatsCitationsFromTopHits() {
        ChunkStore store = new ChunkStore();
        Chunk c1 = new Chunk("idari_birimler.txt", "fakulte_sekreteri", "Fakülte sekreteri Buket Burcu Kambak'tır.", "idari_birimler", 0, 50);
        Chunk c2 = new Chunk("komisyonlar.txt", "erasmus_komisyonu", "Erasmus komisyonu öğrenci değişim programlarını yönetir.", "komisyonlar", 100, 150);
        store.addChunk(c1);
        store.addChunk(c2);

        Hit h1 = new Hit("idari_birimler.txt", "fakulte_sekreteri", 3);
        Hit h2 = new Hit("komisyonlar.txt", "erasmus_komisyonu", 2);

        TemplateAnswerAgent agent = new TemplateAnswerAgent();
        Answer answer = agent.answer(
                List.of("sekreter"),
                List.of(h1, h2),
                store);

        List<String> citations = answer.getCitations();

        assertEquals(2, citations.size());
        assertEquals("idari_birimler.txt:idari_birimler:0-50", citations.get(0));
        assertEquals("komisyonlar.txt:komisyonlar:100-150", citations.get(1));
    }
}


