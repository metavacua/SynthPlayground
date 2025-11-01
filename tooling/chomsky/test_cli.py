"""
Tests for the unified Chomsky toolchain CLI.
"""

import unittest
from unittest.mock import patch
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from tooling.chomsky.cli import main as chomsky_main


class TestCli(unittest.TestCase):

    def setUp(self):
        self.test_plan_file = "test_plan.txt"
        with open(self.test_plan_file, "w") as f:
            f.write("plan_step_complete: Test step")

    def tearDown(self):
        os.remove(self.test_plan_file)

    @patch("tooling.chomsky.cli.LBAValidator.validate")
    @patch("tooling.chomsky.cli.analyze_plan")
    def test_validate_plan_success(self, mock_analyze_plan, mock_validate):
        # Mock the analyzer and validator to return success
        mock_analyze_plan.return_value = {"complexity_class": "P"}
        mock_validate.return_value = (True, "")

        # Call the CLI with the validate-plan command
        with patch.object(
            sys,
            "argv",
            [
                "cli.py",
                "validate-plan",
                self.test_plan_file,
                "--model",
                "A",
                "--complexity",
                "P",
            ],
        ):
            chomsky_main()

        mock_validate.assert_called_once_with("plan_step_complete: Test step", "A")

    @patch("tooling.chomsky.refactor_cs_to_cf.main")
    def test_refactor_orchestration_cs_to_cf(self, mock_refactor_main):
        # Create a dummy file to refactor
        test_file = "test_refactor_file.py"
        with open(test_file, "w") as f:
            f.write("print('hello')")

        # Call the CLI with the refactor command
        with patch.object(
            sys, "argv", ["cli.py", "refactor", test_file, "--strategy", "cs-to-cf"]
        ):
            chomsky_main()

        mock_refactor_main.assert_called_once_with([test_file])

        os.remove(test_file)

    @patch("tooling.chomsky.refactor_cf_to_r.main")
    def test_refactor_orchestration_cf_to_r(self, mock_refactor_main):
        # Create a dummy file to refactor
        test_file = "test_refactor_file.py"
        with open(test_file, "w") as f:
            f.write("print('hello')")

        # Call the CLI with the refactor command
        with patch.object(
            sys, "argv", ["cli.py", "refactor", test_file, "--strategy", "cf-to-r"]
        ):
            chomsky_main()

        mock_refactor_main.assert_called_once_with([test_file])

        os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
