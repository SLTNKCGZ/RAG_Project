import unittest
from typing import Dict, List, Set

from src.model.intent import Intent
from src.writer.heuristic_query_writer import HeuristicQueryWriter


class TestHeuristicQueryWriter(unittest.TestCase):
    """Unit tests for HeuristicQueryWriter class."""

    def setUp(self):
        """Set up test fixtures."""
        pass

    def test_removes_stopwords_and_keeps_content_words(self):
        """Test that stopwords are removed and content words are kept."""
        stopwords: Set[str] = {"ve", "için"}
        writer: HeuristicQueryWriter = HeuristicQueryWriter(stopwords, {})

        terms: List[str] = writer.write(
            "Öğrenci kayıt ve danışman seçimi için adımlar nelerdir?",
            Intent.REGISTRATION,
        )

        # Verify content words are kept and stopwords are removed
        self.assertIn("öğrenci", terms)
        self.assertIn("kayıt", terms)
        self.assertIn("danışman", terms)
        self.assertNotIn("ve", terms)
        self.assertNotIn("için", terms)

    def test_returns_empty_list_for_null_or_empty_question(self):
        """Test that empty list is returned for None or empty question."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})

        self.assertEqual(writer.write(None, Intent.UNKNOWN), [])
        self.assertEqual(writer.write("", Intent.UNKNOWN), [])

    def test_appends_staff_lookup_boosters(self):
        """Test that staff lookup boosters are appended."""
        boosters: Dict[Intent, List[str]] = {
            Intent.STAFF_LOOKUP: ["staff", "advisor", "office"]
        }
        writer: HeuristicQueryWriter = HeuristicQueryWriter({"bilgisi"}, boosters)

        terms: List[str] = writer.write("Danışman bilgisi lazım", Intent.STAFF_LOOKUP)

        # Verify boosters are included
        self.assertIn("staff", terms)
        self.assertIn("advisor", terms)
        self.assertIn("office", terms)

    def test_removes_special_characters(self):
        """Test that special characters are removed."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("Merhaba! @#$ Dünya?", Intent.UNKNOWN)
        
        # No special characters should remain
        for term in terms:
            self.assertTrue(term.replace(" ", "").isalnum() or any(c in "çğıöşüÇĞİÖŞÜ" for c in term))

    def test_lowercases_all_terms(self):
        """Test that all terms are converted to lowercase."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("UPPERCASE WORDS İçinde", Intent.UNKNOWN)
        
        # All should be lowercase
        for term in terms:
            self.assertEqual(term, term.lower())

    def test_handles_complex_query_decomposition(self):
        """Test that complex queries with conjunctions are decomposed."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("Kayıt ve danışman seçimi", Intent.UNKNOWN)
        
        # Should contain terms from both parts
        self.assertIn("kayıt", terms)
        self.assertIn("danışman", terms)
        self.assertIn("seçimi", terms)

    def test_handles_simple_query_without_decomposition(self):
        """Test that simple queries without conjunctions are processed normally."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter({"için"}, {})
        terms: List[str] = writer.write("Danışman bulma", Intent.UNKNOWN)
        
        self.assertIn("danışman", terms)
        self.assertIn("bulma", terms)

    def test_with_none_stopwords(self):
        """Test initialization with None stopwords."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(None, {})
        terms: List[str] = writer.write("Test query", Intent.UNKNOWN)
        
        self.assertIsNotNone(terms)
        self.assertIsInstance(terms, list)

    def test_with_none_intent_boosters(self):
        """Test initialization with None intent boosters."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), None)
        terms: List[str] = writer.write("Test query", Intent.UNKNOWN)
        
        self.assertIsNotNone(terms)
        self.assertIsInstance(terms, list)

    def test_empty_stopwords_set(self):
        """Test with empty stopwords set."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("Test query words", Intent.UNKNOWN)
        
        self.assertGreater(len(terms), 0)

    def test_multiple_intent_boosters(self):
        """Test with multiple intent booster sets."""
        boosters: Dict[Intent, List[str]] = {
            Intent.REGISTRATION: ["register", "enroll"],
            Intent.STAFF_LOOKUP: ["staff", "advisor"],
            Intent.COURSE: ["course", "class"]
        }
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), boosters)
        
        # Test with different intents
        terms_reg = writer.write("Kayıt", Intent.REGISTRATION)
        terms_staff = writer.write("Danışman", Intent.STAFF_LOOKUP)
        
        self.assertIn("register", terms_reg)
        self.assertIn("staff", terms_staff)

    def test_boosters_case_insensitive(self):
        """Test that booster matching is case-insensitive."""
        boosters: Dict[Intent, List[str]] = {
            Intent.STAFF_LOOKUP: ["Staff", "ADVISOR"]
        }
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), boosters)
        terms: List[str] = writer.write("Danışman", Intent.STAFF_LOOKUP)
        
        # Boosters should be included regardless of case
        self.assertTrue(any("staff" in t.lower() or "advisor" in t.lower() for t in terms))

    def test_get_term_weights_functionality(self):
        """Test get_term_weights method."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        weights = writer.get_term_weights("Test query words", Intent.UNKNOWN)
        
        self.assertIsInstance(weights, dict)
        self.assertGreater(len(weights), 0)

    def test_get_term_weights_empty_question(self):
        """Test get_term_weights with empty question."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        weights = writer.get_term_weights("", Intent.UNKNOWN)
        
        self.assertEqual(weights, {})

    def test_get_stemming_stats_functionality(self):
        """Test get_stemming_stats method."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        stats = writer.get_stemming_stats("kitaplar evler masalar")
        
        self.assertIsInstance(stats, dict)
        if stats:  # Only check if not empty
            self.assertIn("total_terms", stats)
            self.assertIn("unique_after_stemming", stats)

    def test_stemming_disabled(self):
        """Test with stemming disabled."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {}, enable_stemming=False)
        terms: List[str] = writer.write("kitaplar kitap", Intent.UNKNOWN)
        
        # With stemming disabled, should keep original forms
        self.assertGreater(len(terms), 0)

    def test_term_weighting_disabled(self):
        """Test with term weighting disabled."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {}, enable_term_weighting=False)
        terms: List[str] = writer.write("test test query", Intent.UNKNOWN)
        
        # Should still return terms, just not weighted
        self.assertGreater(len(terms), 0)

    def test_both_stemming_and_weighting_disabled(self):
        """Test with both stemming and weighting disabled."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(
            set(), {}, 
            enable_stemming=False, 
            enable_term_weighting=False
        )
        terms: List[str] = writer.write("Test query", Intent.UNKNOWN)
        
        self.assertGreater(len(terms), 0)

    def test_duplicate_terms_handling(self):
        """Test handling of duplicate terms in complex queries."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("test ve test", Intent.UNKNOWN)
        
        # Duplicates should be removed
        self.assertEqual(len(terms), 1)
        self.assertEqual(terms[0], "test")

    def test_unicode_turkish_characters(self):
        """Test support for Turkish Unicode characters."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms: List[str] = writer.write("Çağ Ğğ İii Ö Ş Ü", Intent.UNKNOWN)
        
        # Should handle Turkish characters correctly
        self.assertGreater(len(terms), 0)

    def test_whitespace_normalization(self):
        """Test whitespace normalization."""
        writer: HeuristicQueryWriter = HeuristicQueryWriter(set(), {})
        terms1: List[str] = writer.write("Test   query", Intent.UNKNOWN)
        terms2: List[str] = writer.write("Test query", Intent.UNKNOWN)
        
        # Should produce same result regardless of whitespace
        self.assertEqual(terms1, terms2)

    def test_mixed_stopwords_and_boosters(self):
        """Test with both stopwords and boosters."""
        stopwords: Set[str] = {"ve", "için"}
        boosters: Dict[Intent, List[str]] = {
            Intent.REGISTRATION: ["enroll", "register"]
        }
        writer: HeuristicQueryWriter = HeuristicQueryWriter(stopwords, boosters)
        terms: List[str] = writer.write("Kayıt ve danışman için yardım", Intent.REGISTRATION)
        
        self.assertNotIn("ve", terms)
        self.assertNotIn("için", terms)
        self.assertIn("enroll", terms)
        self.assertIn("register", terms)


# Keep old test functions for backward compatibility
def test_removes_stopwords_and_keeps_content_words() -> None:
    stopwords: Set[str] = {"ve", "için"}
    writer: HeuristicQueryWriter = HeuristicQueryWriter(stopwords, {})

    terms: List[str] = writer.write(
        "Öğrenci kayıt ve danışman seçimi için adımlar nelerdir?",
        Intent.REGISTRATION,
    )

    assert "öğrenci" in terms
    assert "kayıt" in terms
    assert "danışman" in terms
    assert "ve" not in terms
    assert "için" not in terms


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

    assert "staff" in terms
    assert "advisor" in terms
    assert "office" in terms


if __name__ == "__main__":
    unittest.main()
