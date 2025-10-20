import unittest
import json
import os

class TestSelfImprovementProtocol(unittest.TestCase):

    def setUp(self):
        """
        Load the self-improvement protocol from the JSON file.
        """
        protocol_path = "protocols/self_improvement/self-improvement.protocol.json"
        with open(protocol_path, "r") as f:
            self.protocol = json.load(f)

    def test_protocol_id(self):
        """
        Test that the protocol has the correct ID.
        """
        self.assertEqual(self.protocol["protocol_id"], "self-improvement-protocol-001")

    def test_rules_exist(self):
        """
        Test that the protocol has the expected number of rules.
        """
        self.assertEqual(len(self.protocol["rules"]), 5)

    def test_associated_tool_exists(self):
        """
        Test that the associated tool exists in the tooling directory.
        """
        tool_path = self.protocol["associated_tools"][0]
        self.assertTrue(os.path.exists(tool_path), f"Tool not found at {tool_path}")

if __name__ == "__main__":
    unittest.main()