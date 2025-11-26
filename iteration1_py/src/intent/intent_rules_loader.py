from typing import List, Dict, Optional
from pathlib import Path

from models import Intent


class IntentRulesLoader:

    def load_rules(self, rules_file_path: Path) -> Dict[Intent, List[str]]:
        try:
            lines: List[str] = rules_file_path.read_text(encoding="utf-8").splitlines()
            return self.__parse_intent_rules(lines)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load intent rules from: {rules_file_path}"
            ) from e

    def __parse_intent_rules(self, lines: List[str]) -> Dict[Intent, List[str]]:

        rules: Dict[Intent, List[str]] = {}
        priority: List[Intent] = []

        in_intent_priority: bool = False
        in_keyword_rules: bool = False

        current_intent: Optional[Intent] = None
        current_keywords: Optional[List[str]] = None

        for line in lines:
            trimmed: str = line.strip()

            # Skip empty or commented lines
            if not trimmed or trimmed.startswith("#"):
                continue

            # Section switches
            if trimmed == "intent_priority:":
                in_intent_priority = True
                in_keyword_rules = False
                continue

            if trimmed == "keyword_rules:":
                in_keyword_rules = True
                in_intent_priority = False
                continue

            # Priority section
            if in_intent_priority and trimmed.startswith("-"):
                intent_name: str = trimmed[1:].strip()
                intent_name = self.__strip_quotes(intent_name)
                intent: Intent = self.__parse_intent_name(intent_name)
                priority.append(intent)
                continue

            # Keyword rules section
            if in_keyword_rules:
                if trimmed.endswith(":") and not trimmed.startswith("-"):
                    # Save previous entry
                    if current_intent is not None and current_keywords is not None:
                        rules[current_intent] = current_keywords

                    # New intent block
                    intent_name: str = trimmed[:-1].strip()
                    current_intent = self.__parse_intent_name(intent_name)
                    current_keywords = []
                    continue

                # Keyword line
                if trimmed.startswith("-") and current_intent is not None:
                    kw: str = trimmed[1:].strip()
                    kw = self.__strip_quotes(kw)
                    current_keywords.append(kw)

        # Save last block
        if current_intent is not None and current_keywords is not None:
            rules[current_intent] = current_keywords

        # Re-order rules based on priority
        ordered_rules: Dict[Intent, List[str]] = {}

        for intent in priority:
            if intent in rules:
                ordered_rules[intent] = rules[intent]

        # Add intents not in priority
        for intent, kw_list in rules.items():
            if intent not in ordered_rules:
                ordered_rules[intent] = kw_list

        return ordered_rules

    def __strip_quotes(self, text: str) -> str:

        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            return text[1:-1]
        return text

    def __parse_intent_name(self, yaml_name: str) -> Intent:
    
        name = yaml_name.upper()

        if name == "REGISTRATION":
            return Intent.Registration
        if name == "STAFF_LOOKUP":
            return Intent.StaffLookup
        if name == "POLICY_FAQ":
            return Intent.PolicyFAQ
        if name == "COURSE":
            return Intent.Course
        if name == "UNKNOWN":
            return Intent.Unknown

        raise ValueError(f"Unknown intent name: {yaml_name}")
