import unittest
import os
import tempfile
import json
import yaml
from unittest.mock import patch

import knowledge_integrator

class TestKnowledgeIntegrator(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.source_file1 = os.path.join(self.test_dir.name, "source1.yaml")
        self.source_file2 = os.path.join(self.test_dir.name, "source2.yaml")
        self.output_file = os.path.join(self.test_dir.name, "output.jsonld")

        self.data1 = {
            '@context': 'protocols/protocol.context.jsonld',
            '@graph': [{'protocol_id': 'PROTO-1', 'description': 'protocol one'}]
        }
        self.data2 = {
            'protocol_id': 'PROTO-2', 'description': 'protocol two'
        }

        with open(self.source_file1, 'w') as f:
            yaml.dump(self.data1, f)
        with open(self.source_file2, 'w') as f:
            yaml.dump(self.data2, f)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_main_integration(self):
        """Test that the main script correctly integrates multiple YAML-LD sources."""
        # Mock sys.argv
        test_args = [
            "knowledge_integrator.py",
            "--source-file", self.source_file1,
            "--source-file", self.source_file2,
            "--output-file", self.output_file
        ]
        with patch('sys.argv', test_args):
            knowledge_integrator.main()

        # Check the output file
        with open(self.output_file, 'r') as f:
            output_data = json.load(f)

        self.assertEqual(output_data['@context'], 'protocols/protocol.context.jsonld')
        self.assertEqual(len(output_data['@graph']), 2)

        # order is not guaranteed, so check for presence of both items
        g = output_data['@graph']
        self.assertTrue(self.data1['@graph'][0] in g)
        self.assertTrue(self.data2 in g)

if __name__ == '__main__':
    unittest.main()
