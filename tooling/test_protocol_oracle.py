import unittest
import os
import json
import shutil
from rdflib import Graph, Literal, Namespace, RDF, RDFS
from protocol_oracle import get_applicable_protocols, get_rules_for_protocols

PROTOCOL = Namespace("https://www.aida.org/protocol#")

class TestProtocolOracle(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_protocol_oracle_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.g = Graph()
        self.g.bind("protocol", PROTOCOL)

        # Create a dummy python protocol file for testing applicability
        self.py_protocol_path = os.path.join(self.test_dir, "conditional.protocol.py")
        with open(self.py_protocol_path, "w") as f:
            f.write('def is_applicable(context):\n')
            f.write('    return context.get("task_type") == "refactor"\n')


    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_applicable_protocols(self):
        """Tests that the correct protocols are identified based on context."""
        # Setup graph data
        p1_uri = PROTOCOL["static-proto"]
        p2_uri = PROTOCOL["conditional-proto"]
        self.g.add((p1_uri, RDF.type, PROTOCOL.Protocol))
        self.g.add((p2_uri, RDF.type, PROTOCOL.Protocol))
        self.g.add((p2_uri, PROTOCOL.hasApplicabilityCondition, Literal(self.py_protocol_path)))

        # Test case 1: Context matches conditional protocol
        context_match = {"task_type": "refactor"}
        applicable = get_applicable_protocols(self.g, context_match)
        self.assertIn(str(p1_uri), applicable)
        self.assertIn(str(p2_uri), applicable)

        # Test case 2: Context does not match conditional protocol
        context_no_match = {"task_type": "docs"}
        applicable = get_applicable_protocols(self.g, context_no_match)
        self.assertIn(str(p1_uri), applicable)
        self.assertNotIn(str(p2_uri), applicable)

    def test_get_rules_for_protocols(self):
        """Tests that rules are correctly retrieved for a given protocol."""
        p1_uri = PROTOCOL["proto-with-rules"]
        r1_uri = PROTOCOL["rule-1"]
        self.g.add((p1_uri, RDF.type, PROTOCOL.Protocol))
        self.g.add((p1_uri, PROTOCOL.hasRule, r1_uri))
        self.g.add((r1_uri, RDFS.label, Literal("rule-1")))
        self.g.add((r1_uri, PROTOCOL.description, Literal("Rule 1 description")))
        self.g.add((r1_uri, PROTOCOL.enforcement, Literal("Rule 1 enforcement")))

        rules = get_rules_for_protocols(self.g, [str(p1_uri)])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["rule_id"], "rule-1")

if __name__ == "__main__":
    unittest.main()