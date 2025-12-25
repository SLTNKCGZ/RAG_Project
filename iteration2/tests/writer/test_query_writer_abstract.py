import unittest
from abc import ABC
from src.writer.query_writer_abstract import QueryWriter
from src.model.intent import Intent


class ConcreteQueryWriter(QueryWriter):
    """Concrete implementation for testing abstract class."""
    
    def write(self, question: str, intent: Intent):
        """Implementation for testing."""
        return [question]


class TestQueryWriterAbstract(unittest.TestCase):
    """Unit tests for QueryWriter abstract class."""

    def setUp(self):
        """Set up test fixtures."""
        self.writer = ConcreteQueryWriter()

    def test_is_abstract_class(self):
        """Test that QueryWriter is abstract."""
        self.assertTrue(issubclass(QueryWriter, ABC))

    def test_concrete_implementation_can_be_instantiated(self):
        """Test that concrete implementation can be instantiated."""
        self.assertIsNotNone(self.writer)
        self.assertIsInstance(self.writer, QueryWriter)

    def test_write_method_exists(self):
        """Test that write method exists."""
        self.assertTrue(hasattr(self.writer, 'write'))
        self.assertTrue(callable(getattr(self.writer, 'write')))

    def test_write_method_accepts_question_and_intent(self):
        """Test that write method accepts question and intent parameters."""
        question = "Test question"
        intent = Intent.UNKNOWN
        result = self.writer.write(question, intent)
        self.assertIsNotNone(result)

    def test_write_method_returns_list(self):
        """Test that write method returns a list."""
        result = self.writer.write("Test", Intent.UNKNOWN)
        self.assertIsInstance(result, list)

    def test_abstract_method_must_be_implemented(self):
        """Test that abstract method must be implemented."""
        try:
            # Attempting to create abstract class directly should fail
            abstract_instance = QueryWriter()
            self.fail("Should not be able to instantiate abstract class")
        except TypeError:
            # Expected behavior
            pass

    def test_write_with_none_question(self):
        """Test write method with None question."""
        result = self.writer.write(None, Intent.UNKNOWN)
        self.assertIsNotNone(result)

    def test_write_with_empty_question(self):
        """Test write method with empty question."""
        result = self.writer.write("", Intent.UNKNOWN)
        self.assertIsNotNone(result)

    def test_write_with_different_intents(self):
        """Test write method with different intent types."""
        intents = [Intent.UNKNOWN, Intent.REGISTRATION, Intent.STAFF_LOOKUP]
        for intent in intents:
            result = self.writer.write("Test question", intent)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
