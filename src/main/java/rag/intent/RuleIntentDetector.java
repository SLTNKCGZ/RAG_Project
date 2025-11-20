package main.java.rag.intent;

import java.util.List;
import java.util.Map;
import main.java.rag.model.Intent;

/**
 * Rule-based implementation of IntentDetector with priority support.
 * Intent priority is determined inside the Intent enum (getPriority()).
 */
public class RuleIntentDetector implements IntentDetector {

    private final Map<Intent, List<String>> rules;

    public RuleIntentDetector(Map<Intent, List<String>> rules) {
        this.rules = rules;
    }

    @Override
    public Intent detect(String question) {
        if (question == null || question.trim().isEmpty()) {
            return Intent.UNKNOWN;
        }

        String lower = question.toLowerCase();

        return rules.keySet()
                .stream()
                .sorted((i1, i2) -> Integer.compare(i1.getPriority(), i2.getPriority()))
                .filter(intent -> matches(lower, intent))
                .findFirst()
                .orElse(Intent.UNKNOWN);
    }

    private boolean matches(String text, Intent intent) {
        List<String> keywords = rules.get(intent);
        if (keywords == null) return false;

        for (String kw : keywords) {
            if (kw != null && text.contains(kw.toLowerCase())) {
                return true;
            }
        }
        return false;
    }
}