package com.cse3063f25grp1.intent;

import com.cse3063f25grp1.model.Intent;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

class RuleIntentDetectorTest {

    @Test
    void detectsIntentAccordingToPriorityOrderWhenMultipleMatch() {
        Map<Intent, List<String>> rules = new HashMap<>();
        rules.put(Intent.Registration, Arrays.asList("kayıt", "ders kaydı"));
        rules.put(Intent.Course, Arrays.asList("ders", "course"));

        // Önce Course sonra Registration gelecek şekilde priority
        List<Intent> priority = Arrays.asList(Intent.Course, Intent.Registration);

        RuleIntentDetector detector = new RuleIntentDetector(rules, priority);

        String question = "Ders kaydı nasıl yapılır?";
        Intent detected = detector.detect(question);

        // Her iki intent için de anahtar kelime geçiyor, fakat priority'de Course önde
        assertSame(Intent.Course, detected);
    }

    @Test
    void returnsUnknownForEmptyOrNullQuestion() {
        Map<Intent, List<String>> rules = Collections.emptyMap();
        List<Intent> priority = Collections.singletonList(Intent.Registration);

        RuleIntentDetector detector = new RuleIntentDetector(rules, priority);

        assertEquals(Intent.Unknown, detector.detect(null));
        assertEquals(Intent.Unknown, detector.detect("   "));
    }
}


