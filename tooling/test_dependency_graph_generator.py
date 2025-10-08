import unittest
import os
import json
from unittest.mock import patch, mock_open

# Import the function to be tested
from tooling.dependency_graph_generator import generate_dependency_graph

class TestDependencyGraphGenerator(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.output_dir = "knowledge_core"
        self.output_file = os.path.join(self.output_dir, "dependency_graph.json")
        self.requirements_file = "requirements.txt"

        # Clean up any old output files before each test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    @patch('os.path.exists', return_value=True)
    def test_graph_generation_from_mock_requirements(self, mock_path_exists):
        """
        Tests that the dependency graph is generated correctly from a mock
        requirements.txt file content.
        """
        # Mock the content of requirements.txt
        mock_req_content = "package-a==1.0\npackage-b>=2.0\n# A comment\n\npackage-c"

        # Use patch to mock open() for reading requirements.txt and writing the output
        m = mock_open(read_data=mock_req_content)
        with patch("builtins.open", m) as mock_file:
            generate_dependency_graph()

            # Verify that the output file was attempted to be written to
            m.assert_any_call(self.output_file, 'w')

            # Check the content that was written to the mock file handle
            handle = m()
            written_content = "".join(call.args[0] for call in handle.write.mock_calls)
            data = json.loads(written_content)

            self.assertEqual(data["project_name"], "SynthPlayground")

            # Check for expected nodes
            node_ids = {node["id"] for node in data["nodes"]}
            self.assertIn("root", node_ids)
            self.assertIn("package-a", node_ids)
            self.assertIn("package-b", node_ids)
            self.assertIn("package-c", node_ids)
            self.assertEqual(len(node_ids), 4)

            # Check for expected edges
            edge_targets = {edge["to"] for edge in data["edges"]}
            self.assertEqual(edge_targets, {"package-a", "package-b", "package-c"})
            self.assertEqual(len(data["edges"]), 3)

    def test_no_requirements_file(self):
        """
        Tests that the script handles the absence of a requirements.txt file gracefully.
        """
        # Temporarily rename the requirements file to simulate its absence
        if os.path.exists(self.requirements_file):
            os.rename(self.requirements_file, self.requirements_file + ".bak")

        try:
            generate_dependency_graph()
            # The script should not create the output file if the input is missing
            self.assertFalse(os.path.exists(self.output_file))
        finally:
            # Restore the requirements file
            if os.path.exists(self.requirements_file + ".bak"):
                os.rename(self.requirements_file + ".bak", self.requirements_file)

if __name__ == "__main__":
    unittest.main()