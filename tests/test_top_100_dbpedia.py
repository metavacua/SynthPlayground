import unittest
import json
import os
import sys
from unittest.mock import patch
from ddt import ddt, data

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.external_api_client import ExternalApiClient

# Load the mock data
mock_data_path = os.path.join(os.path.dirname(__file__), "data", "mock_dbpedia_data.json")
with open(mock_data_path, "r") as f:
    mock_data = json.load(f)

@ddt
class TestDbpediaClientDDT(unittest.TestCase):
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

class TestDbpediaClient(unittest.TestCase):
    def setUp(self):
        self.client = ExternalApiClient("dbpedia_client")

    @patch("tooling.external_api_client.subprocess.run")
    def test_get_resource_type(self, mock_subprocess_run):
        """
        Tests that the DBPedia client can fetch the rdf:type for a resource.
        """
        entry = "Software_engineering"
        expected_type = "owl:Thing"

        # Configure the mock to return the expected type
        mock_process = unittest.mock.Mock()
        mock_process.stdout = expected_type
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_subprocess_run.return_value = mock_process

        result = self.client.execute(["get_type", entry])
        self.assertEqual(result, expected_type)

        # Verify that the subprocess was called with the correct command
        mock_subprocess_run.assert_called_with(
            ["python3", "dbpedia_client.py", "get_type", entry],
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
