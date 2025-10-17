import unittest
import subprocess
from unittest.mock import patch, call
from tooling.pre_submit_check import main as pre_submit_check_main, run_command

class TestPreSubmitCheck(unittest.TestCase):

    @patch('tooling.pre_submit_check.subprocess.run')
    def test_main_runs_lint(self, mock_run):
        """Tests that the main function runs the lint command."""
        pre_submit_check_main()
        mock_run.assert_called_once_with("make lint", check=True, shell=True, text=True, capture_output=True)

    @patch('tooling.pre_submit_check.subprocess.run', side_effect=subprocess.CalledProcessError(1, "cmd", "output", "error"))
    def test_run_command_failure(self, mock_run):
        """Tests that run_command exits on a failed command."""
        with self.assertRaises(SystemExit):
            run_command("failing command", "Test Failure")

if __name__ == "__main__":
    unittest.main()