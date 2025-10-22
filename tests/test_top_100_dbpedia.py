import unittest
import json
import os
from unittest.mock import patch
from ddt import ddt, data

from tooling.external_api_client import ExternalApiClient

# Load the mock data
mock_data_path = os.path.join(os.path.dirname(__file__), "data", "mock_dbpedia_data.json")
with open(mock_data_path, "r") as f:
    mock_data = json.load(f)

@ddt
class TestDbpediaClient(unittest.TestCase):
    def setUp(self):
        self.client = ExternalApiClient("dbpedia_client")

    @data(*mock_data)
    @patch("tooling.external_api_client.subprocess.run")
    def test_get_abstract(self, test_data, mock_subprocess_run):
        """
        Tests that the DBPedia client can fetch abstracts for various entries.
        """
        entry = test_data["entry"]
        abstract = test_data["abstract"]

        # Configure the mock to return the expected abstract
        mock_process = unittest.mock.Mock()
        mock_process.stdout = abstract
        mock_process.stderr = "" if abstract else "No abstract found"
        mock_process.returncode = 0 if abstract else 1
        mock_subprocess_run.return_value = mock_process

        if abstract:
            result = self.client.execute(["get", entry])
            self.assertEqual(result, abstract)
        else:
            with self.assertRaises(Exception):
                self.client.execute(["get", entry])

        # Verify that the subprocess was called with the correct command
        mock_subprocess_run.assert_called_with(
            ["python3", "dbpedia_client.py", "get", entry],
            capture_output=True,
            text=True,
        )

if __name__ == "__main__":
    unittest.main()
