package com.cse3063f25grp1.intent;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import com.cse3063f25grp1.model.Intent;

public class IntentRulesLoader {

    public Map<Intent, List<String>> loadRules(Path rulesFilePath) {
        try {
            List<String> lines = Files.readAllLines(rulesFilePath);
            return parseIntentRules(lines);
        } catch (IOException e) {
            throw new RuntimeException("Failed to load intent rules from: " + rulesFilePath, e);
        }
    }

    private Map<Intent, List<String>> parseIntentRules(List<String> lines) {
        Map<Intent, List<String>> rules = new LinkedHashMap<>();
        List<Intent> priority = new ArrayList<>();
        boolean inIntentPriority = false;
        boolean inKeywordRules = false;
        Intent currentIntent = null;
        List<String> currentKeywords = null;

        for (String line : lines) {
            String trimmed = line.trim();

            if (trimmed.isEmpty() || trimmed.startsWith("#")) {
                continue;
            }

            if (trimmed.equals("intent_priority:")) {
                inIntentPriority = true;
                inKeywordRules = false;
                continue;
            }

            if (trimmed.equals("keyword_rules:")) {
                inKeywordRules = true;
                inIntentPriority = false;
                continue;
            }

            if (inIntentPriority && trimmed.startsWith("-")) {
                String intentName = trimmed.substring(1).trim();
                if (intentName.startsWith("\"") && intentName.endsWith("\"")) {
                    intentName = intentName.substring(1, intentName.length() - 1);
                }
                Intent intent = parseIntentName(intentName);
                priority.add(intent);
            }

            if (inKeywordRules) {
                if (trimmed.endsWith(":") && !trimmed.startsWith("-")) {
                    if (currentIntent != null && currentKeywords != null) {
                        rules.put(currentIntent, currentKeywords);
                    }

                    String intentName = trimmed.substring(0, trimmed.length() - 1).trim();
                    currentIntent = parseIntentName(intentName);
                    currentKeywords = new ArrayList<>();
                } else if (trimmed.startsWith("-")) {
                    if (currentIntent != null && currentKeywords != null) {
                        String keyword = trimmed.substring(1).trim();
                        if (keyword.startsWith("\"") && keyword.endsWith("\"")) {
                            keyword = keyword.substring(1, keyword.length() - 1);
                        }
                        currentKeywords.add(keyword);
                    }
                }
            }
        }

        if (currentIntent != null && currentKeywords != null) {
            rules.put(currentIntent, currentKeywords);
        }

        // Priority'ye göre sırala
        Map<Intent, List<String>> orderedRules = new LinkedHashMap<>();
        for (Intent intent : priority) {
            if (rules.containsKey(intent)) {
                orderedRules.put(intent, rules.get(intent));
            }
        }

        // Priority'de olmayan intent'leri de ekle
        for (Map.Entry<Intent, List<String>> entry : rules.entrySet()) {
            if (!orderedRules.containsKey(entry.getKey())) {
                orderedRules.put(entry.getKey(), entry.getValue());
            }
        }

        return orderedRules;
    }

    private Intent parseIntentName(String yamlName) {
        switch (yamlName.toUpperCase()) {
            case "REGISTRATION":
                return Intent.Registration;
            case "STAFF_LOOKUP":
                return Intent.StaffLookup;
            case "POLICY_FAQ":
                return Intent.PolicyFAQ;
            case "COURSE":
                return Intent.Course;
            case "UNKNOWN":
                return Intent.Unknown;
            default:
                throw new IllegalArgumentException("Unknown intent name: " + yamlName);
        }
    }
}
