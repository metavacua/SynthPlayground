import unittest
import os
import json
import shutil
from unittest.mock import patch, MagicMock
from tooling.log_failure import log_catastrophic_failure

class TestLogFailure(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_log_failure_dir"
        os.makedirs(os.path.join(self.test_dir, "logs"), exist_ok=True)
        self.log_path = os.path.join(self.test_dir, "logs", "activity.log.jsonl")

        # Patch the Logger's __init__ to set the log_path
        def mock_init(self, schema_path=None):
            self.log_path = TestLogFailure.log_path

        patcher = patch('utils.logger.Logger.__init__', mock_init)
        patcher.start()
        # Bind the log_path to the class for the mock_init to use
        TestLogFailure.log_path = self.log_path
        self.addCleanup(patcher.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('utils.logger.Logger.log')
    def test_log_catastrophic_failure(self, mock_log):
        """Tests that the catastrophic failure is logged correctly."""
        log_catastrophic_failure()

        mock_log.assert_called_once()
        args, kwargs = mock_log.call_args

        self.assertEqual(kwargs['phase'], "Phase 8")
        self.assertEqual(kwargs['action_type'], "SYSTEM_FAILURE")
        self.assertIn("reset_all", kwargs['action_details']['tool_name'])
        self.assertEqual(kwargs['outcome_status'], "FAILURE")

if __name__ == "__main__":
    unittest.main()