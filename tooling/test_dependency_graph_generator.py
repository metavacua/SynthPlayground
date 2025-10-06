import unittest
import os
import json
import shutil
from tooling.dependency_graph_generator import find_package_json_files, parse_dependencies, generate_dependency_graph

class TestDependencyGraphGenerator(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = "temp_test_repo"
        os.makedirs(os.path.join(self.test_dir, 'project_a'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'project_b', 'node_modules', 'some_dep'), exist_ok=True)

        # Create mock package.json files
        self.pkg_a_path = os.path.join(self.test_dir, 'project_a', 'package.json')
        with open(self.pkg_a_path, 'w') as f:
            json.dump({
                "name": "project-a",
                "dependencies": {
                    "project-b": "1.0.0",
                    "external-lib": "2.0.0"
                }
            }, f)

        self.pkg_b_path = os.path.join(self.test_dir, 'project_b', 'package.json')
        with open(self.pkg_b_path, 'w') as f:
            json.dump({
                "name": "project-b",
                "devDependencies": {
                    "jest": "29.0.0"
                }
            }, f)

        # Create a package.json inside node_modules that should be ignored
        ignored_pkg_path = os.path.join(self.test_dir, 'project_b', 'node_modules', 'some_dep', 'package.json')
        with open(ignored_pkg_path, 'w') as f:
            json.dump({"name": "ignored-dep"}, f)

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_find_package_json_files(self):
        """Test that it finds correct package.json files and ignores node_modules."""
        found_files = find_package_json_files(self.test_dir)
        self.assertEqual(len(found_files), 2)
        self.assertIn(self.pkg_a_path, found_files)
        self.assertIn(self.pkg_b_path, found_files)

    def test_parse_dependencies(self):
        """Test parsing a single package.json file."""
        parsed_info = parse_dependencies(self.pkg_a_path)
        self.assertIsNotNone(parsed_info)
        self.assertEqual(parsed_info['package_name'], 'project-a')
        self.assertIn('project-b', parsed_info['dependencies'])
        self.assertIn('external-lib', parsed_info['dependencies'])

    def test_generate_dependency_graph(self):
        """Test the full graph generation logic."""
        graph = generate_dependency_graph(self.test_dir)

        # Check nodes
        self.assertEqual(len(graph['nodes']), 2)
        node_names = {node['id'] for node in graph['nodes']}
        self.assertEqual(node_names, {'project-a', 'project-b'})

        # Check edges (should only contain internal dependencies)
        self.assertEqual(len(graph['edges']), 1)
        edge = graph['edges'][0]
        self.assertEqual(edge['source'], 'project-a')
        self.assertEqual(edge['target'], 'project-b')

if __name__ == '__main__':
    unittest.main()