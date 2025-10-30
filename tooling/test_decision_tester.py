import unittest
import os
import subprocess
from unittest.mock import patch, mock_open

class TestDecisionTester(unittest.TestCase):

    def setUp(self):
        self.test_file_content = """
- id: DMT-001
  scenario: A test scenario.
  context: []
  expected_action:
    tool: a_tool
    args:
      arg1: value1
"""
        os.makedirs("decision_tests", exist_ok=True)
        self.test_file_path = "decision_tests/test_decision_tester_dummy.yaml"
        with open(self.test_file_path, "w") as f:
            f.write(self.test_file_content)

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_run_test_pass(self):
        result = subprocess.run(
            ["python3", "tooling/decision_tester.py", self.test_file_path, "a_tool", '{"arg1": "value1"}'],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--- Test DMT-001 Passed ---", result.stdout)

    def test_run_test_fail(self):
        result = subprocess.run(
            ["python3", "tooling/decision_tester.py", self.test_file_path, "a_tool", '{"arg1": "wrong_value"}'],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--- Test DMT-001 Failed ---", result.stdout)


if __name__ == '__main__':
    unittest.main()
