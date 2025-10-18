"""
Unit tests for the protocol_updater.py script.

This test suite verifies that the protocol updater tool can correctly
find and modify protocol source files in a controlled, temporary
environment. It ensures that tools can be added to protocols and that
edge cases like duplicate additions are handled gracefully.
"""

import unittest
import os
import json
import tempfile
import shutil
from tooling.protocol_updater import add_tool_to_protocol, find_protocol_file


class TestProtocolUpdater(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with a mock protocols structure."""
        self.test_dir = tempfile.mkdtemp()
        self.protocols_dir_orig = "protocols/"

        # Create a mock protocols directory
        self.mock_protocols_dir = os.path.join(self.test_dir, "protocols/")
        os.makedirs(self.mock_protocols_dir)

        # Point the updater script's PROTOCOLS_DIR to our mock directory
        import tooling.protocol_updater

        tooling.protocol_updater.PROTOCOLS_DIR = self.mock_protocols_dir

        # Create a mock protocol file
        self.protocol_file_path = os.path.join(
            self.mock_protocols_dir, "test.protocol.json"
        )
        self.protocol_id = "test-protocol-001"
        self.initial_data = {
            "protocol_id": self.protocol_id,
            "description": "A test protocol.",
            "associated_tools": ["existing_tool"],
        }
        with open(self.protocol_file_path, "w") as f:
            json.dump(self.initial_data, f, indent=2)

    def tearDown(self):
        """Clean up the temporary directory and restore original config."""
        shutil.rmtree(self.test_dir)
        import tooling.protocol_updater

        tooling.protocol_updater.PROTOCOLS_DIR = self.protocols_dir_orig

    def test_find_protocol_file_success(self):
        """Verify that a protocol file can be found by its ID."""
        found_path = find_protocol_file(self.protocol_id, self.mock_protocols_dir)
        self.assertEqual(found_path, self.protocol_file_path)

    def test_find_protocol_file_not_found(self):
        """Verify that None is returned for a non-existent protocol ID."""
        found_path = find_protocol_file("non-existent-id", self.mock_protocols_dir)
        self.assertIsNone(found_path)

    def test_add_tool_to_protocol_success(self):
        """Verify that a new tool can be successfully added to a protocol."""
        new_tool = "new_tool_123"
        add_tool_to_protocol(self.protocol_id, new_tool, self.mock_protocols_dir)

        # Read the file back and check the contents
        with open(self.protocol_file_path, "r") as f:
            data = json.load(f)

        self.assertIn(new_tool, data["associated_tools"])
        self.assertIn("existing_tool", data["associated_tools"])
        self.assertEqual(len(data["associated_tools"]), 2)

    def test_add_duplicate_tool(self):
        """Verify that adding an existing tool does not create a duplicate."""
        existing_tool = "existing_tool"
        add_tool_to_protocol(self.protocol_id, existing_tool, self.mock_protocols_dir)

        with open(self.protocol_file_path, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data["associated_tools"]), 1)
        self.assertEqual(data["associated_tools"].count(existing_tool), 1)


if __name__ == "__main__":
    unittest.main()
