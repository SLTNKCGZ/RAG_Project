package com.cse3063f25grp1.writer;

import org.junit.jupiter.api.Test;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

class HeuristicQueryWriterTest {

    @Test
    void removesStopwordsAndKeepsContentWords() {
        Set<String> stopwords = new HashSet<>();
        stopwords.add("ve");
        stopwords.add("için");
        HeuristicQueryWriter writer = new HeuristicQueryWriter(stopwords);

        List<String> terms = writer.write("Öğrenci kayıt ve danışman seçimi için adımlar nelerdir?");

        assertEquals(List.of("öğrenci", "kayıt", "danışman", "seçimi", "adımlar", "nelerdir"), terms);
    }

    @Test
    void returnsEmptyListForNullOrEmptyQuestion() {
        HeuristicQueryWriter writer = new HeuristicQueryWriter(Set.of());

        assertEquals(List.of(), writer.write(null));
        assertEquals(List.of(), writer.write(""));
    }
}


