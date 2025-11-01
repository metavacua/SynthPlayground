import unittest
from tooling.dependency_graph_generator_logic import (
    parse_package_json_content,
    parse_requirements_txt_content,
    generate_dependency_graph_from_projects,
)


class TestDependencyGraphGenerator(unittest.TestCase):
    def test_parse_package_json_content(self):
        content = """
{
    "name": "my-project",
    "dependencies": {
        "react": "17.0.2"
    }
}
"""
        info = parse_package_json_content(content, "/path/to/package.json")
        self.assertEqual(info["project_name"], "my-project")
        self.assertEqual(info["dependencies"], ["react"])

    def test_parse_requirements_txt_content(self):
        content = """
requests==2.25.1
numpy
"""
        info = parse_requirements_txt_content(
            content, "/path/to/requirements.txt", "/path"
        )
        self.assertEqual(info["project_name"], "to")
        self.assertEqual(info["dependencies"], ["requests", "numpy"])

    def test_generate_dependency_graph_from_projects(self):
        projects = [
            {
                "project_name": "project-a",
                "path": "/path/to/project-a",
                "dependencies": ["project-b", "react"],
                "type": "javascript",
            },
            {
                "project_name": "project-b",
                "path": "/path/to/project-b",
                "dependencies": ["numpy"],
                "type": "python",
            },
        ]
        graph = generate_dependency_graph_from_projects(projects)
        self.assertEqual(len(graph["nodes"]), 4)
        self.assertEqual(len(graph["edges"]), 3)


if __name__ == "__main__":
    unittest.main()
