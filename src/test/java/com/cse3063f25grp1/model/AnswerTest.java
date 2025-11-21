package com.cse3063f25grp1.model;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Tests for {@link Answer} focused on how it will be used in the RAG pipeline:
 * - final answer text that explains a registration/policy question
 * - citations that point to specific document sections (docId:sectionId:start-end)
 * - single line formatting that will be printed by {@code Main}.
 */
class AnswerTest {

    @Test
    void toSingleLine_keepsRegistrationAnswerText_whenNoCitationsPresent() {
        // simulate a final answer for a registration FAQ
        Answer answer = new Answer("Ders kaydı, akademik takvimde belirtilen kayıt haftasında yapılır.");

        assertEquals(
                "Ders kaydı, akademik takvimde belirtilen kayıt haftasında yapılır.",
                answer.toSingleLine());
    }

    @Test
    void toSingleLine_appendsPolicyCitationsInChunkCitationFormat() {
        // answer generated from two different chunks of policy documents
        Answer answer = new Answer("Devamsızlık sınırı %70 devam zorunluluğudur.");
        answer.addCitation("ogrenci_el_kitabi.pdf:attendance_rules:120-260");
        answer.addCitation("yonerge_2024.pdf:madde_15:10-80");

        assertEquals(
                "Devamsızlık sınırı %70 devam zorunluluğudur. See: ogrenci_el_kitabi.pdf:attendance_rules:120-260, yonerge_2024.pdf:madde_15:10-80",
                answer.toSingleLine());
    }

    @Test
    void constructor_preservesGivenCitationsForCourseInfoScenario() {
        // course information synthesized from multiple sections of the same document
        List<String> citations = List.of(
                "cse3063_syllabus.pdf:intro:0-120",
                "cse3063_syllabus.pdf:grading:300-420");

        Answer answer = new Answer("CSE3063 dersinde proje bileşeni ve final sınavı bulunmaktadır.", citations);

        assertEquals(
                "CSE3063 dersinde proje bileşeni ve final sınavı bulunmaktadır. See: cse3063_syllabus.pdf:intro:0-120, cse3063_syllabus.pdf:grading:300-420",
                answer.toSingleLine());
    }
}


