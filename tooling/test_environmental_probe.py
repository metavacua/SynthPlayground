import unittest
import os
import requests
from unittest.mock import patch, MagicMock
from tooling.environmental_probe import (
    probe_filesystem,
    probe_network,
    probe_environment_variables,
)


class TestEnvironmentalProbe(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_environmental_probe_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir("..")
        os.rmdir(self.test_dir)

    def test_probe_filesystem(self):
        """Tests the filesystem probe."""
        status, msg, latency = probe_filesystem()
        self.assertEqual(status, "PASS")
        self.assertIn("successful", msg)

    @patch("tooling.environmental_probe.requests.head")
    def test_probe_network_success(self, mock_head):
        """Tests the network probe with a successful connection."""
        mock_head.return_value = MagicMock(status_code=200)
        status, msg, latency = probe_network()
        self.assertEqual(status, "PASS")
        self.assertIn("Successfully connected", msg)

    @patch(
        "tooling.environmental_probe.requests.head",
        side_effect=requests.exceptions.Timeout,
    )
    def test_probe_network_timeout(self, mock_head):
        """Tests the network probe with a timeout."""
        status, msg, latency = probe_network()
        self.assertEqual(status, "FAIL")
        self.assertIn("timed out", msg)

    def test_probe_environment_variables(self):
        """Tests the environment variable probe."""
        # The PATH variable should always be present in a standard environment
        status, msg, _ = probe_environment_variables()
        self.assertEqual(status, "PASS")
        self.assertIn("'PATH' is present", msg)

    @patch.dict(os.environ, {}, clear=True)
    def test_probe_environment_variables_missing(self):
        """Tests the environment variable probe when PATH is missing."""
        status, msg, _ = probe_environment_variables()
        self.assertEqual(status, "WARN")
        self.assertIn("'PATH' is not set", msg)


if __name__ == "__main__":
    unittest.main()
