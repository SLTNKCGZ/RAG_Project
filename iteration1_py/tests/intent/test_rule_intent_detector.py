
from typing import Dict, List

from src.model.intent import Intent
from src.intent.rule_intent_detector import RuleIntentDetector


def test_detects_intent_according_to_priority_order_when_multiple_match():
    rules: Dict[Intent, List[str]] = {
        Intent.Registration: ["kayıt", "ders kaydı"],
        Intent.Course: ["ders", "course"]
    }

    priority: List[Intent] = [Intent.Course, Intent.Registration]

    detector: RuleIntentDetector = RuleIntentDetector(rules, priority)

    question: str = "Ders kaydı nasıl yapılır?"
    detected: Intent = detector.detect(question)

    assert detected == Intent.Course


def test_returns_unknown_for_empty_or_null_question():
    rules: Dict[Intent, List[str]] = {}
    priority: List[Intent] = [Intent.Registration]

    detector: RuleIntentDetector = RuleIntentDetector(rules, priority)

    assert detector.detect(None) == Intent.Unknown
    assert detector.detect("   ") == Intent.Unknown
