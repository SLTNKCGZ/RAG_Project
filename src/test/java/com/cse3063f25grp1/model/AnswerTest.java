package com.cse3063f25grp1.model;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Tests for {@link Answer} class - citation formatting for RAG pipeline.
 */
class AnswerTest {

    @Test
    void toSingleLine_formatsAnswerWithCitations() {
        // Test basic citation formatting using real CSE department data
        Answer answer = new Answer("Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir.");
        answer.addCitation("erasmus_bilgileri.pdf:koordinator:5-15");
        answer.addCitation("bolum_rehberi.pdf:uluslararasi_iliskiler:200-250");

        assertEquals("Erasmus koordinatörü Dr. Öğr. Üyesi Ali Haydar Özer'dir. See: erasmus_bilgileri.pdf:koordinator:5-15, bolum_rehberi.pdf:uluslararasi_iliskiler:200-250",
                    answer.toSingleLine());
    }

    @Test
    void addCitation_and_hasCitations_workCorrectly() {
        // Test citation management methods using CSE department staff data
        Answer answer = new Answer("Fakülte sekreteri Buket Burcu Kambak'ın ofisi M1-307'dedir.");

        // Initially no citations
        assertEquals(false, answer.hasCitations());

        // Add citation from administrative units document
        answer.addCitation("idari_birimler.pdf:fakulte_sekreteri:1-10");
        assertTrue(answer.hasCitations());

        // Add another citation from department guide
        answer.addCitation("bolum_rehberi.pdf:iletisim:50-80");
        assertEquals(2, answer.getCitations().size());
    }
}