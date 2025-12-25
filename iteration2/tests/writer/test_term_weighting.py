import unittest
from src.writer.term_weighting import TermWeighting


class TestTermWeighting(unittest.TestCase):
    """Unit tests for TermWeighting class."""

    def setUp(self):
        """Set up test fixtures."""
        self.weighting = TermWeighting(
            tf_weight=1.0,
            booster_weight=2.0,
            base_weight=1.0
        )

    def test_calculate_weights_single_term(self):
        """Test weight calculation for single term."""
        terms = ["kitap"]
        boosted_terms = []
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        self.assertIn("kitap", weights)
        self.assertGreater(weights["kitap"], 0)

    def test_calculate_weights_multiple_terms(self):
        """Test weight calculation for multiple terms."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        self.assertEqual(len(weights), 3)
        self.assertIn("kitap", weights)
        self.assertIn("evi", weights)
        self.assertIn("masa", weights)

    def test_calculate_weights_term_frequency(self):
        """Test that term frequency affects weight."""
        terms = ["kitap", "kitap", "evi"]
        boosted_terms = []
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        # "kitap" appears twice, so should have higher weight
        self.assertGreater(weights["kitap"], weights["evi"])

    def test_calculate_weights_with_boosted_terms(self):
        """Test that boosted terms get higher weight."""
        terms = ["kitap", "evi"]
        boosted_terms = ["kitap"]
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        # "kitap" is boosted, so should have higher weight
        self.assertGreater(weights["kitap"], weights["evi"])

    def test_calculate_weights_booster_multiplier(self):
        """Test booster weight multiplier."""
        terms = ["kitap", "evi", "kitap"]
        boosted_terms = ["evi"]
        weights1 = TermWeighting(tf_weight=1.0, booster_weight=1.0, base_weight=1.0).calculate_weights(terms, boosted_terms)
        weights2 = TermWeighting(tf_weight=1.0, booster_weight=2.0, base_weight=1.0).calculate_weights(terms, boosted_terms)
        # With higher booster weight, "evi" should be relatively higher
        self.assertGreater(weights2["evi"] / weights2["kitap"], weights1["evi"] / weights1["kitap"])

    def test_calculate_weights_empty_terms(self):
        """Test weight calculation with empty terms list."""
        terms = []
        boosted_terms = []
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        self.assertEqual(weights, {})

    def test_calculate_weights_case_insensitive_boosters(self):
        """Test that boosters are matched case-insensitively."""
        terms = ["kitap", "evi"]
        boosted_terms = ["KITAP"]
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        # "kitap" should still be boosted despite case difference
        self.assertGreater(weights["kitap"], weights["evi"])

    def test_rank_terms_descending_order(self):
        """Test that rank_terms returns terms in descending weight order."""
        terms = ["kitap", "evi", "masa", "kitap"]
        boosted_terms = []
        ranked = self.weighting.rank_terms(terms, boosted_terms)
        # Should be sorted in descending order by weight
        weights = [w for _, w in ranked]
        self.assertEqual(weights, sorted(weights, reverse=True))

    def test_rank_terms_format(self):
        """Test that rank_terms returns list of (term, weight) tuples."""
        terms = ["kitap", "evi"]
        boosted_terms = []
        ranked = self.weighting.rank_terms(terms, boosted_terms)
        self.assertIsInstance(ranked, list)
        for item in ranked:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], float)

    def test_rank_terms_empty_list(self):
        """Test rank_terms with empty list."""
        ranked = self.weighting.rank_terms([], [])
        self.assertEqual(ranked, [])

    def test_get_top_terms_default_k(self):
        """Test get_top_terms with default k value."""
        terms = ["kitap", "evi", "masa"] * 10
        boosted_terms = []
        top_terms = self.weighting.get_top_terms(terms, boosted_terms)
        self.assertEqual(len(top_terms), 3)  # Only 3 unique terms

    def test_get_top_terms_custom_k(self):
        """Test get_top_terms with custom k value."""
        terms = ["kitap", "evi", "masa", "sandalye", "taş"]
        boosted_terms = []
        top_terms = self.weighting.get_top_terms(terms, boosted_terms, top_k=3)
        self.assertEqual(len(top_terms), 3)

    def test_get_top_terms_k_greater_than_unique(self):
        """Test get_top_terms when k is greater than unique terms."""
        terms = ["kitap", "evi"]
        boosted_terms = []
        top_terms = self.weighting.get_top_terms(terms, boosted_terms, top_k=10)
        self.assertEqual(len(top_terms), 2)

    def test_get_top_terms_empty_list(self):
        """Test get_top_terms with empty list."""
        top_terms = self.weighting.get_top_terms([], [], top_k=5)
        self.assertEqual(top_terms, [])

    def test_get_top_terms_returns_strings(self):
        """Test that get_top_terms returns only term strings."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        top_terms = self.weighting.get_top_terms(terms, boosted_terms, top_k=2)
        for term in top_terms:
            self.assertIsInstance(term, str)

    def test_get_weight_stats_contains_keys(self):
        """Test that get_weight_stats returns all required keys."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        stats = self.weighting.get_weight_stats(terms, boosted_terms)
        required_keys = ["total_terms", "avg_weight", "max_weight", "min_weight"]
        for key in required_keys:
            self.assertIn(key, stats)

    def test_get_weight_stats_total_terms(self):
        """Test that total_terms count is correct."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        stats = self.weighting.get_weight_stats(terms, boosted_terms)
        self.assertEqual(stats["total_terms"], 3)

    def test_get_weight_stats_max_min_relationship(self):
        """Test that max_weight >= min_weight."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        stats = self.weighting.get_weight_stats(terms, boosted_terms)
        self.assertGreaterEqual(stats["max_weight"], stats["min_weight"])

    def test_get_weight_stats_avg_calculation(self):
        """Test that average weight is calculated correctly."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = []
        stats = self.weighting.get_weight_stats(terms, boosted_terms)
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        expected_avg = sum(weights.values()) / len(weights)
        self.assertAlmostEqual(stats["avg_weight"], expected_avg, places=5)

    def test_get_weight_stats_empty_list(self):
        """Test get_weight_stats with empty list."""
        stats = self.weighting.get_weight_stats([], [])
        self.assertEqual(stats["total_terms"], 0)
        self.assertEqual(stats["avg_weight"], 0)
        self.assertEqual(stats["max_weight"], 0)
        self.assertEqual(stats["min_weight"], 0)

    def test_weight_consistency(self):
        """Test that same input produces same weights."""
        terms = ["kitap", "evi", "masa"]
        boosted_terms = ["kitap"]
        weights1 = self.weighting.calculate_weights(terms, boosted_terms)
        weights2 = self.weighting.calculate_weights(terms, boosted_terms)
        self.assertEqual(weights1, weights2)

    def test_calculate_weights_with_duplicates(self):
        """Test weight calculation handles duplicates correctly."""
        terms = ["kitap", "kitap", "kitap", "evi"]
        boosted_terms = []
        weights = self.weighting.calculate_weights(terms, boosted_terms)
        # "kitap" frequency is 3, "evi" is 1, so "kitap" should have higher weight
        self.assertGreater(weights["kitap"], weights["evi"])

    def test_booster_weight_parameter_effect(self):
        """Test that booster_weight parameter affects results."""
        terms = ["kitap", "evi"]
        boosted_terms = ["evi"]
        
        weighting1 = TermWeighting(tf_weight=1.0, booster_weight=1.0, base_weight=1.0)
        weighting2 = TermWeighting(tf_weight=1.0, booster_weight=5.0, base_weight=1.0)
        
        weights1 = weighting1.calculate_weights(terms, boosted_terms)
        weights2 = weighting2.calculate_weights(terms, boosted_terms)
        
        # With higher booster weight, the ratio should be different
        ratio1 = weights1["evi"] / weights1["kitap"]
        ratio2 = weights2["evi"] / weights2["kitap"]
        self.assertGreater(ratio2, ratio1)


if __name__ == "__main__":
    unittest.main()
