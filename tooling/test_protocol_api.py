import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from rdflib import Graph
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.protocol_api import ProtocolAPI

class TestProtocolAPI(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_protocol_api_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.protocols_dir = os.path.join(self.test_dir, "protocols")
        os.makedirs(self.protocols_dir, exist_ok=True)
        self.knowledge_graph_path = os.path.join(self.test_dir, "protocols.ttl")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("tooling.protocol_api.create_protocol")
    def test_create_protocol(self, mock_create_protocol):
        api = ProtocolAPI(protocols_dir=self.protocols_dir)
        api.create_protocol("Test Protocol")
        mock_create_protocol.assert_called_once_with("Test Protocol", self.protocols_dir)

    @patch("tooling.protocol_api.update_version")
    def test_update_protocol_version(self, mock_update_version):
        api = ProtocolAPI()
        api.update_protocol_version("test-protocol", "1.1.0")
        mock_update_version.assert_called_once_with("test-protocol", "1.1.0")

    @patch("tooling.protocol_api.get_applicable_protocols")
    @patch("tooling.protocol_api.get_rules_for_protocols")
    def test_get_applicable_rules(self, mock_get_rules, mock_get_protocols):
        api = ProtocolAPI(knowledge_graph_path=self.knowledge_graph_path)
        context = {"task_type": "refactor"}
        mock_get_protocols.return_value = ["proto1", "proto2"]
        mock_get_rules.return_value = ["rule1", "rule2"]

        rules = api.get_applicable_rules(context)

        mock_get_protocols.assert_called_once_with(api.graph, context)
        mock_get_rules.assert_called_once_with(api.graph, ["proto1", "proto2"])
        self.assertEqual(rules, ["rule1", "rule2"])

if __name__ == "__main__":
    unittest.main()
