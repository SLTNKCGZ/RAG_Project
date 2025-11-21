package com.cse3063f25grp1.writer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import com.cse3063f25grp1.model.Intent;

public class HeuristicQueryWriter implements QueryWriter {

    private static final Locale TR_LOCALE = new Locale("tr", "TR");
    private static final String SPLIT_REGEX = "\\s+";
    private static final String CLEAN_REGEX = "[^\\p{L}0-9 ]";
    private final Set<String> stopwords;
    private final Map<Intent, List<String>> intentBoosters;

    public HeuristicQueryWriter(Set<String> stopwords, Map<Intent, List<String>> intentBoosters) {
        if (stopwords == null) {
            this.stopwords = Collections.emptySet();
        } else {
            this.stopwords = stopwords.stream()
                    .filter(s -> s != null && !s.isBlank())
                    .map(s -> s.toLowerCase(TR_LOCALE))
                    .collect(Collectors.toUnmodifiableSet());
        }
        if (intentBoosters == null) {
            this.intentBoosters = Collections.emptyMap();
        } else {
            Map<Intent, List<String>> normalized = new LinkedHashMap<>();
            for (Map.Entry<Intent, List<String>> entry : intentBoosters.entrySet()) {
                List<String> normalizedTokens = entry.getValue().stream()
                        .filter(s -> s != null && !s.isBlank())
                        .map(s -> s.toLowerCase(TR_LOCALE))
                        .collect(Collectors.toUnmodifiableList());
                normalized.put(entry.getKey(), normalizedTokens);
            }
            this.intentBoosters = Collections.unmodifiableMap(normalized);
        }
    }

    @Override
    public List<String> write(String question, Intent intent) {
        if (question == null || question.isBlank()) {
            return Collections.emptyList();
        }

        String cleaned = question.toLowerCase(TR_LOCALE).replaceAll(CLEAN_REGEX, " ");
        List<String> parts = Arrays.asList(cleaned.split(SPLIT_REGEX));

        LinkedHashSet<String> orderedTerms = new LinkedHashSet<>();
        for (String p : parts) {
            String token = p.trim();
            if (token.isEmpty()) {
                continue;
            }
            if (stopwords.contains(token)) {
                continue;
            }
            orderedTerms.add(token);
        }

        Intent resolvedIntent = intent == null ? Intent.Unknown : intent;
        List<String> boosters = intentBoosters.get(resolvedIntent);
        if (boosters != null) {
            for (String booster : boosters) {
                orderedTerms.add(booster);
            }
        }

        return new ArrayList<>(orderedTerms);
    }
}