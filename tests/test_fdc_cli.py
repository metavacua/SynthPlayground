import os
import unittest
import subprocess
import json
import shutil
from unittest.mock import patch, MagicMock

# This is a bit of a hack to make sure we can import the CLI script
# even though it's not in a standard package structure.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling import fdc_cli

class TestFdcCli(unittest.TestCase):

    def setUp(self):
        """Set up a clean environment for each test."""
        self.test_dir = "test_workspace"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)

        # Initialize a git repository for testing
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit"], check=True, capture_output=True)

    def tearDown(self):
        """Clean up the environment after each test."""
        os.chdir("..")
        shutil.rmtree(self.test_dir)

    @patch('tooling.fdc_cli.subprocess.run')
    @patch('tooling.fdc_cli.uuid.uuid4')
    def test_start_standard_task(self, mock_uuid4, mock_subprocess):
        """Test starting a standard, single-branch task."""
        mock_uuid4.return_value.__str__.return_value = 'test-uuid'

        parser = fdc_cli.create_parser()
        args = parser.parse_args(['start', 'My new standard task'])
        fdc_cli.handle_start(args)

        # Check that git checkout -b was called correctly
        expected_branch = 'feature/task-test-uuid'
        mock_subprocess.assert_called_with(
            ['git', 'checkout', '-b', expected_branch],
            check=True, capture_output=True, text=True
        )

        # Check that the log file was written correctly
        self.assertTrue(os.path.exists(fdc_cli.LOG_FILE_PATH))
        with open(fdc_cli.LOG_FILE_PATH, 'r') as f:
            log_entry = json.load(f)
            self.assertEqual(log_entry['action_type'], 'TASK_START')
            self.assertEqual(log_entry['details']['task_id'], 'test-uuid')
            self.assertEqual(log_entry['details']['branch'], expected_branch)
            self.assertEqual(log_entry['details']['description'], 'My new standard task')

if __name__ == '__main__':
    unittest.main()