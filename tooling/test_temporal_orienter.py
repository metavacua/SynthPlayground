import unittest
import os
import shutil
from tooling.temporal_orienter import log_orientation_entry, LOG_FILE_PATH
from unittest.mock import patch


class TestTemporalOrienter(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and a dummy log file for testing."""
        self.test_dir = "temp_orienter_test"
        self.knowledge_core_dir = os.path.join(self.test_dir, "knowledge_core")
        os.makedirs(self.knowledge_core_dir, exist_ok=True)

        # Point the LOG_FILE_PATH to our temporary file for the duration of the test
        self.temp_log_path = os.path.join(
            self.knowledge_core_dir, "temporal_orientation.md"
        )

        # Create an empty file to append to
        with open(self.temp_log_path, "w") as f:
            f.write("# Temporal Orientation Log\n\n---\n\n")

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch(
        "tooling.temporal_orienter.LOG_FILE_PATH",
        new_callable=lambda: "temp_orienter_test/knowledge_core/temporal_orientation.md",
    )
    def test_log_orientation_entry_appends_correctly(self, mock_log_path):
        """Test that log entries are correctly formatted and appended to the file."""

        # First entry
        summary1 = "React 19 introduces a new compiler and automatic memoization."
        log_orientation_entry(summary1)

        with open(self.temp_log_path, "r") as f:
            content = f.read()

        self.assertIn("## Entry:", content)
        self.assertIn("UTC", content)
        self.assertIn(summary1, content)

        # Second entry
        summary2 = "Python 3.13 enhances the GIL for better multi-core performance."
        log_orientation_entry(summary2)

        with open(self.temp_log_path, "r") as f:
            content_after_second_log = f.read()

        self.assertIn(summary1, content_after_second_log)
        self.assertIn(summary2, content_after_second_log)
        self.assertEqual(
            content_after_second_log.count("## Entry:"),
            2,
            "Should have two distinct entries",
        )


if __name__ == "__main__":
    unittest.main()
