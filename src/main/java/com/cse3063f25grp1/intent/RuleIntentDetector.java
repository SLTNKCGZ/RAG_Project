package com.cse3063f25grp1.intent;

import java.util.List;
import java.util.Map;
import com.cse3063f25grp1.model.Intent;

public class RuleIntentDetector implements IntentDetector {

    private final Map<Intent, List<String>> rules;
    private final List<Intent> priorityOrder;

    // Yeni constructor: priorityOrder ConfigLoader tarafından gönderilecek
    public RuleIntentDetector(Map<Intent, List<String>> rules,
            List<Intent> priorityOrder) {
        this.rules = rules;
        this.priorityOrder = priorityOrder;
    }

    @Override
    public Intent detect(String question) {
        if (question == null || question.trim().isEmpty()) {
            return Intent.Unknown;
        }

        String lower = question.toLowerCase();

        // INTENT PRIORITY SIRASINA GÖRE KONTROL
        for (Intent intent : priorityOrder) {
            List<String> keywords = rules.get(intent);
            if (keywords == null)
                continue;

            for (String keyword : keywords) {
                if (keyword != null && lower.contains(keyword.toLowerCase())) {
                    return intent;
                }
            }
        }

        return Intent.Unknown;
    }
}