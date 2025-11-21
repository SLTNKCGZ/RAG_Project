package com.cse3063f25grp1.writer;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

import com.cse3063f25grp1.model.Intent;

class HeuristicQueryWriterTest {

    @Test
    void removesStopwordsAndKeepsContentWords() {
        Set<String> stopwords = new HashSet<>();
        stopwords.add("ve");
        stopwords.add("için");
        HeuristicQueryWriter writer = new HeuristicQueryWriter(stopwords, Map.of());

        List<String> terms = writer.write(
                "Öğrenci kayıt ve danışman seçimi için adımlar nelerdir?",
                Intent.Registration);

        assertEquals(List.of("öğrenci", "kayıt", "danışman", "seçimi", "adımlar", "nelerdir"), terms);
    }

    @Test
    void returnsEmptyListForNullOrEmptyQuestion() {
        HeuristicQueryWriter writer = new HeuristicQueryWriter(Set.of(), Map.of());

        assertEquals(List.of(), writer.write(null, Intent.Unknown));
        assertEquals(List.of(), writer.write("", Intent.Unknown));
    }

    @Test
    void appendsStaffLookupBoosters() {
        HeuristicQueryWriter writer = new HeuristicQueryWriter(
                Set.of("bilgisi"),
                Map.of(Intent.StaffLookup, List.of("staff", "advisor", "office")));

        List<String> terms = writer.write("Danışman bilgisi lazım", Intent.StaffLookup);

        assertEquals(List.of("danışman", "lazım", "staff", "advisor", "office"), terms);
    }
}
