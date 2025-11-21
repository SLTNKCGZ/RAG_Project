package com.cse3063f25grp1.answer;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TemplateAnswerAgentTest {

    @Test
    void selectsSentenceThatContainsAllQueryTerms() {
        ChunkStore store = new ChunkStore();
        String text = "Kayıt haftası Eylül ayındadır. Öğrenci kayıt işlemleri öğrenci bilgi sistemi üzerinden yapılır. " +
                "Danışman onayı gerekmektedir.";
        Chunk chunk = new Chunk("doc1", "c1", text, "sec1", 0, text.length());
        store.addChunk(chunk);
        store.setDocumentTitle("doc1", "Kayıt Bilgileri");

        Hit hit = new Hit("doc1", "c1", 5);

        TemplateAnswerAgent agent = new TemplateAnswerAgent();
        Answer answer = agent.answer(
                List.of("öğrenci", "kayıt", "işlemleri"),
                List.of(hit),
                store);

        String answerText = answer.getText();
        String lower = answerText.toLowerCase();

        // Cevap, kaynak açıklamasıyla başlamalı
        assertTrue(answerText.startsWith("Bu cevap \"Kayıt Bilgileri\" başlıklı belgenin sec1 bölümünden alınmıştır."));
        // Seçilen cümle, tüm query terimlerini içermeli
        assertTrue(lower.contains("öğrenci"));
        assertTrue(lower.contains("kayıt"));
        assertTrue(lower.contains("işlemleri"));
    }

    @Test
    void formatsCitationsFromTopHits() {
        ChunkStore store = new ChunkStore();
        Chunk c1 = new Chunk("doc1", "c1", "metin1", "sec1", 0, 10);
        Chunk c2 = new Chunk("doc2", "c2", "metin2", "sec2", 11, 30);
        store.addChunk(c1);
        store.addChunk(c2);

        Hit h1 = new Hit("doc1", "c1", 3);
        Hit h2 = new Hit("doc2", "c2", 2);

        TemplateAnswerAgent agent = new TemplateAnswerAgent();
        Answer answer = agent.answer(
                List.of("metin"),
                List.of(h1, h2),
                store);

        List<String> citations = answer.getCitations();

        assertEquals(2, citations.size());
        assertEquals("doc1:sec1:0-10", citations.get(0));
        assertEquals("doc2:sec2:11-30", citations.get(1));
    }
}


