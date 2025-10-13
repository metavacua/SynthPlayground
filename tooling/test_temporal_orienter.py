import unittest
from tooling.temporal_orienter import get_dbpedia_summary

class TestTemporalOrienter(unittest.TestCase):

    def test_get_dbpedia_summary_success(self):
        """
        Tests that get_dbpedia_summary returns a non-empty string for a valid topic.
        """
        summary = get_dbpedia_summary("Python_(programming_language)")
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        self.assertNotIn("No summary found", summary)
        self.assertNotIn("An error occurred", summary)

    def test_get_dbpedia_summary_not_found(self):
        """
        Tests that get_dbpedia_summary returns a 'not found' message for an invalid topic.
        """
        summary = get_dbpedia_summary("NonExistentTopic12345")
        self.assertIn("No summary found for topic", summary)

if __name__ == '__main__':
    unittest.main()