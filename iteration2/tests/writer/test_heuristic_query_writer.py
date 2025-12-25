from typing import Dict, List, Set

from src.model.intent import Intent
from src.writer.heuristic_query_writer import HeuristicQueryWriter


def test_removes_stopwords_and_keeps_content_words() -> None:
    stopwords: Set[str] = {"ve", "için"}
    writer: HeuristicQueryWriter = HeuristicQueryWriter(stopwords, {})

    terms: List[str] = writer.write(
        "Öğrenci kayıt ve danışman seçimi için adımlar nelerdir?",
        Intent.REGISTRATION,
    )

    assert terms == ["öğrenci", "kayıt", "danışman", "seçimi", "adımlar", "nelerdir"]


def test_returns_empty_list_for_null_or_empty_question() -> None:
    writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})

    assert writer.write(None, Intent.UNKNOWN) == []
    assert writer.write("", Intent.UNKNOWN) == []


def test_appends_staff_lookup_boosters() -> None:
    boosters: Dict[Intent, List[str]] = {
        Intent.STAFF_LOOKUP: ["staff", "advisor", "office"]
    }
    writer: HeuristicQueryWriter = HeuristicQueryWriter({"bilgisi"}, boosters)

    terms: List[str] = writer.write("Danışman bilgisi lazım", Intent.STAFF_LOOKUP)

    assert terms == ["danışman", "lazım", "staff", "advisor", "office"]
