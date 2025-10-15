import unittest
import subprocess
import json
import os

class TestComplexityAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set up a dummy grammar file for testing."""
        self.grammar_file = "test_grammar.txt"
        with open(self.grammar_file, "w") as f:
            f.write("S -> a S | b")

    def tearDown(self):
        """Clean up the dummy grammar file."""
        os.remove(self.grammar_file)

    def test_analyzer_right_linear_success(self):
        """Test the complexity analyzer with a simple right-linear grammar that should succeed."""
        input_string = "aaab"
        command = [
            "python3",
            "-m",
            "tooling.complexity_analyzer",
            self.grammar_file,
            input_string,
            "--json"
        ]

        # We need to suppress the noisy output from the recognizer's print statements
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"STDERR: {result.stderr}")

        output = json.loads(result.stdout)

        self.assertEqual(output['grammar_type'], 'Right-Linear')
        self.assertTrue(output['recognized'])
        self.assertIn('time_complexity', output['metrics'])
        self.assertIn('space_complexity', output['metrics'])
        self.assertGreater(output['metrics']['time_complexity'], 0)
        self.assertGreaterEqual(output['metrics']['space_complexity'], 0)

    def test_analyzer_right_linear_failure(self):
        """Test the complexity analyzer with a simple right-linear grammar that should fail."""
        input_string = "abca"
        command = [
            "python3",
            "-m",
            "tooling.complexity_analyzer",
            self.grammar_file,
            input_string,
            "--json"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"STDERR: {result.stderr}")

        output = json.loads(result.stdout)

        self.assertEqual(output['grammar_type'], 'Right-Linear')
        self.assertFalse(output['recognized'])
        self.assertGreater(output['metrics']['time_complexity'], 0)


if __name__ == "__main__":
    unittest.main()