package main.java.rag.intent;

import java.util.List;
import java.util.Map;
import main.java.rag.model.Intent;

public class RuleIntentDetector implements IntentDetector {

    private final Map<Intent, List<String>> rules;

    public RuleIntentDetector(Map<Intent, List<String>> rules) {
        this.rules = rules;
    }

    @Override
    public Intent detect(String question) {
        if (question == null) {
            return Intent.Unknown;
        }

        String lower = question.toLowerCase();

        for (Map.Entry<Intent, List<String>> entry : rules.entrySet()) {
            for (String keyword : entry.getValue()) {
                if (lower.contains(keyword.toLowerCase())) {
                    return entry.getKey();
                }
            }
        }

        return Intent.Unknown;
    }
}