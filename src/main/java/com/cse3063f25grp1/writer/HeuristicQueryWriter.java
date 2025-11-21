package com.cse3063f25grp1.writer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.Set;

public class HeuristicQueryWriter implements QueryWriter {

    private final Set<String> stopwords;

    public HeuristicQueryWriter(Set<String> stopwords) {
        this.stopwords = stopwords;
    }

    @Override
    public List<String> write(String question) {
        if (question == null || question.isEmpty()) {
            return new ArrayList<>();
        }

        // Temizle → tokenize et
        String cleaned = question
                .toLowerCase(new Locale("tr", "TR"))
                .replaceAll("[^\\p{L}0-9 ]", " ");

        List<String> parts = Arrays.asList(cleaned.split("\\s+"));

        List<String> result = new ArrayList<>();

        for (String p : parts) {
            if (p.isBlank())
                continue;
            if (stopwords.contains(p))
                continue;
            result.add(p);
        }

        return result;
    }
}