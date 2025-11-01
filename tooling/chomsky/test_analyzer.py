"""
Tests for the constructive code analyzer.
"""

import unittest
from unittest.mock import patch
from tooling.chomsky.analyzer import CodeAnalyzer


class TestCodeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.test_code = """
def not_recursive(n):
    return n + 1

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
"""

    @patch("tooling.chomsky.analyzer.get_abstract")
    def test_analyze(self, mock_get_abstract):
        # Mock the DBPedia client to avoid network calls
        mock_get_abstract.return_value = "Mocked abstract"

        analyzer = CodeAnalyzer(self.test_code)
        analysis = analyzer.analyze()

        self.assertEqual(analysis["not_recursive"]["recursion_type"], "none")
        self.assertEqual(analysis["factorial"]["recursion_type"], "primitive")
        self.assertEqual(analysis["ackermann"]["recursion_type"], "general")

        # Check that the enrichment was called for the recursive functions
        self.assertIn("enrichment", analysis["factorial"])
        self.assertIn("enrichment", analysis["ackermann"])
        self.assertEqual(mock_get_abstract.call_count, 2)


if __name__ == "__main__":
    unittest.main()
