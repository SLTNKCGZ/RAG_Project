package com.cse3063f25grp1.answer;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.cse3063f25grp1.data.ChunkStore;
import com.cse3063f25grp1.model.Answer;
import com.cse3063f25grp1.model.Chunk;
import com.cse3063f25grp1.model.Hit;

class SimpleAnswerAgentTest {

    @Test
    void selectsSentenceWithMostQueryTerms() {
        ChunkStore store = new ChunkStore();
        String text = "Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir. E-posta adresi haydar.ozer@marmara.edu.tr'dir. " +
                "Erasmus başvuruları bölüm koordinatörü üzerinden yapılır.";
        Chunk chunk = new Chunk("erasmus.txt", "koordinator", text, "erasmus_bilgileri", 0, text.length());
        store.addChunk(chunk);

        Hit hit = new Hit("erasmus.txt", "koordinator", 5);

        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer = agent.answer(
                List.of("erasmus", "koordinatörü"),
                List.of(hit),
                store);

        String answerText = answer.getText();

        // Should select the sentence with most query terms
        assertTrue(answerText.contains("Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir"));
        assertTrue(answerText.startsWith("Your answer:"));
    }

    @Test
    void formatsCitationCorrectly() {
        ChunkStore store = new ChunkStore();
        Chunk chunk = new Chunk("test.txt", "section1", "Test content.", "test_section", 10, 25);
        store.addChunk(chunk);

        Hit hit = new Hit("test.txt", "section1", 3);

        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer = agent.answer(
                List.of("test"),
                List.of(hit),
                store);

        List<String> citations = answer.getCitations();

        assertEquals(1, citations.size());
        assertEquals("test.txt:test_section:10-25", citations.get(0));
    }

    @Test
    void fallbackToFirstSentenceWhenNoQueryTermsMatch() {
        ChunkStore store = new ChunkStore();
        String text = "First sentence with no matching terms. Second sentence also no match. Third sentence.";
        Chunk chunk = new Chunk("test.txt", "section1", text, "test_section", 0, text.length());
        store.addChunk(chunk);

        Hit hit = new Hit("test.txt", "section1", 1);

        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer = agent.answer(
                List.of("nonexistent", "terms"),
                List.of(hit),
                store);

        String answerText = answer.getText();

        // Should fallback to first sentence
        assertTrue(answerText.contains("First sentence with no matching terms"));
        assertTrue(answerText.startsWith("Your answer:"));
    }

    @Test
    void handlesEmptyTopHits() {
        ChunkStore store = new ChunkStore();

        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer = agent.answer(
                List.of("test"),
                List.of(),
                store);

        assertEquals("Üzgünüm, sorunuza cevap bulamadım.", answer.getText());
        assertTrue(answer.getCitations().isEmpty());
    }

    @Test
    void handlesNullChunk() {
        ChunkStore store = new ChunkStore();
        // Don't add chunk to store

        Hit hit = new Hit("nonexistent.txt", "section1", 1);

        SimpleAnswerAgent agent = new SimpleAnswerAgent();
        Answer answer = agent.answer(
                List.of("test"),
                List.of(hit),
                store);

        assertEquals("Üzgünüm, sorunuza ait detaylı metni bulamadım.", answer.getText());
        assertTrue(answer.getCitations().isEmpty());
    }
}