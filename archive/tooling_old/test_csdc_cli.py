import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from tooling.csdc_cli import main as csdc_main

class TestCsdcCli(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_csdc_cli_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.plan_file = os.path.join(self.test_dir, "plan.txt")
        with open(self.plan_file, "w") as f:
            f.write("set_plan\nThis is a test plan.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('tooling.csdc_cli.analyze_plan')
    @patch('tooling.csdc_cli.MasterControlGraph.validate_plan_for_model')
    def test_successful_validation(self, mock_validate, mock_analyze):
        """Tests successful validation for a compliant plan."""
        mock_analyze.return_value = {"complexity_class": "P"}
        mock_validate.return_value = (True, "")

        with patch('sys.argv', ['tooling/csdc_cli.py', self.plan_file, '--model', 'A', '--complexity', 'P']):
            csdc_main()

        mock_analyze.assert_called_once_with(self.plan_file, return_results=True)
        mock_validate.assert_called_once()

    @patch('tooling.csdc_cli.analyze_plan', return_value={"complexity_class": "EXP"})
    def test_complexity_mismatch(self, mock_analyze):
        """Tests that the CLI exits on a complexity mismatch."""
        with patch('sys.argv', ['tooling/csdc_cli.py', self.plan_file, '--model', 'A', '--complexity', 'P']):
            with self.assertRaises(SystemExit):
                csdc_main()

    @patch('tooling.csdc_cli.analyze_plan', return_value={"complexity_class": "P"})
    @patch('tooling.csdc_cli.MasterControlGraph.validate_plan_for_model', return_value=(False, "Invalid command"))
    def test_model_validation_failure(self, mock_validate, mock_analyze):
        """Tests that the CLI exits on a model validation failure."""
        with patch('sys.argv', ['tooling/csdc_cli.py', self.plan_file, '--model', 'A', '--complexity', 'P']):
            with self.assertRaises(SystemExit):
                csdc_main()

    def test_file_not_found(self):
        """Tests that the CLI exits if the plan file is not found."""
        with patch('sys.argv', ['tooling/csdc_cli.py', 'non_existent.txt', '--model', 'A', '--complexity', 'P']):
            with self.assertRaises(SystemExit):
                csdc_main()

if __name__ == "__main__":
    unittest.main()