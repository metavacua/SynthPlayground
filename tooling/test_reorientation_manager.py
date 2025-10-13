import unittest
from unittest.mock import patch, mock_open
import os
import json
from tooling.reorientation_manager import main as reorientation_main

class TestReorientationManager(unittest.TestCase):

    def setUp(self):
        """Set up test files and cleanup afterwards."""
        self.old_agents_path = "AGENTS.md.old.test"
        self.new_agents_path = "AGENTS.md.new.test"
        self.orientations_path = "knowledge_core/temporal_orientations.json"
        self.trigger_path = "deep_research_required.json"

        # Ensure cleanup happens before each test
        self.cleanup_files()

    def tearDown(self):
        """Clean up created files after tests."""
        self.cleanup_files()

    def cleanup_files(self):
        for path in [self.old_agents_path, self.new_agents_path, self.trigger_path, self.orientations_path]:
            if os.path.exists(path):
                if os.path.isdir(path):
                    os.rmdir(os.path.dirname(path))
                else:
                    os.remove(path)
        # Clean up directory if it's empty
        if os.path.exists(os.path.dirname(self.orientations_path)) and not os.listdir(os.path.dirname(self.orientations_path)):
            os.rmdir(os.path.dirname(self.orientations_path))


    @patch("subprocess.run")
    def test_temporal_orientation_triggered(self, mock_subprocess_run):
        """Test that temporal orientation is triggered for new concepts."""
        old_content = '{"protocol_id": "test-proto-1"}'
        new_content = '{"protocol_id": "test-proto-1"} {"protocol_id": "test-proto-2"}'

        with open(self.old_agents_path, "w") as f:
            f.write(old_content)
        with open(self.new_agents_path, "w") as f:
            f.write(new_content)

        # Mock the return value of the temporal orienter
        mock_subprocess_run.return_value.stdout = "This is a summary for test-proto-2."
        mock_subprocess_run.return_value.returncode = 0

        # Run the manager
        with patch('sys.argv', ['reorientation_manager.py', '--old-agents-file', self.old_agents_path, '--new-agents-file', self.new_agents_path]):
            reorientation_main()

        # Check that the orientations file was created with the correct content
        self.assertTrue(os.path.exists(self.orientations_path))
        with open(self.orientations_path, "r") as f:
            data = json.load(f)
        self.assertIn("test-proto-2", data)
        self.assertEqual(data["test-proto-2"], "This is a summary for test-proto-2.")

        # Ensure deep research was NOT triggered
        self.assertFalse(os.path.exists(self.trigger_path))

    @patch("subprocess.run")
    def test_deep_research_triggered(self, mock_subprocess_run):
        """Test that deep research is triggered for significant new concepts."""
        old_content = '{"protocol_id": "existing-protocol"}'
        # Add a new protocol with a keyword that should trigger deep research
        new_content = '{"protocol_id": "existing-protocol"} {"protocol_id": "new-FDC-protocol"}'

        with open(self.old_agents_path, "w") as f:
            f.write(old_content)
        with open(self.new_agents_path, "w") as f:
            f.write(new_content)

        # Mock the return value of the temporal orienter
        mock_subprocess_run.return_value.stdout = "This is a summary for the new FDC protocol."
        mock_subprocess_run.return_value.returncode = 0

        # Run the manager
        with patch('sys.argv', ['reorientation_manager.py', '--old-agents-file', self.old_agents_path, '--new-agents-file', self.new_agents_path]):
            reorientation_main()

        # Check that the deep research trigger file was created
        self.assertTrue(os.path.exists(self.trigger_path))
        with open(self.trigger_path, "r") as f:
            data = json.load(f)
        self.assertEqual(data["topic"], "new-FDC-protocol")

    def test_no_changes_detected(self):
        """Test that no action is taken when there are no new concepts."""
        content = '{"protocol_id": "test-proto-1"}'
        with open(self.old_agents_path, "w") as f:
            f.write(content)
        with open(self.new_agents_path, "w") as f:
            f.write(content)

        # Run the manager
        with patch('sys.argv', ['reorientation_manager.py', '--old-agents-file', self.old_agents_path, '--new-agents-file', self.new_agents_path]):
            reorientation_main()

        # Check that no files were created
        self.assertFalse(os.path.exists(self.orientations_path))
        self.assertFalse(os.path.exists(self.trigger_path))

if __name__ == '__main__':
    unittest.main()