import unittest
import os
import json
import shutil
from unittest.mock import patch
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.protocol_manager import create_protocol, update_version, run_tests

class TestProtocolManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_protocol_manager_dir"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_protocol(self):
        create_protocol("Test Protocol", self.test_dir)
        protocol_file = os.path.join(self.test_dir, "test-protocol.protocol.json")
        self.assertTrue(os.path.exists(protocol_file))
        with open(protocol_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["protocol_id"], "test-protocol")
        self.assertEqual(data["version"], "1.0.0")

    def test_update_version(self):
        protocol_file = os.path.join(self.test_dir, "test-protocol.protocol.json")
        with open(protocol_file, "w") as f:
            json.dump({"protocol_id": "test-protocol", "version": "1.0.0"}, f)

        # To make update_version work, we need to be in a directory that has a `protocols` subdirectory.
        # So we'll create one.
        os.makedirs(os.path.join(self.test_dir, "protocols"), exist_ok=True)
        shutil.move(protocol_file, os.path.join(self.test_dir, "protocols", "test-protocol.protocol.json"))

        # We also need to change the current working directory
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        update_version("test-protocol", "1.1.0")
        os.chdir(original_cwd)

        with open(os.path.join(self.test_dir, "protocols", "test-protocol.protocol.json"), "r") as f:
            data = json.load(f)
        self.assertEqual(data["version"], "1.1.0")

    @patch("os.system")
    def test_run_tests(self, mock_system):
        run_tests()
        mock_system.assert_called_once_with("python3 tests/protocols/test_runner.py")

if __name__ == "__main__":
    unittest.main()
