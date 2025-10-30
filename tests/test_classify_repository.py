import unittest
import os
import json
import subprocess

class TestClassifyRepository(unittest.TestCase):

    def setUp(self):
        """Set up a mock environment for testing."""
        self.test_dir = "tests/temp_repo"
        self.ast_dir = os.path.join(self.test_dir, "knowledge_core/asts")
        self.output_file = os.path.join(self.test_dir, "report.json")
        os.makedirs(self.ast_dir, exist_ok=True)

        # Create mock AST files
        self.mock_asts = {
            "regular.py.json": {
                "type": "A", "children": [{"type": "b"}, {"type": "C", "children": [{"type": "d"}]}]
            },
            "context_free.py.json": {
                "type": "A", "children": [{"type": "B"}, {"type": "B"}]
            }
        }
        for filename, ast_data in self.mock_asts.items():
            with open(os.path.join(self.ast_dir, filename), "w") as f:
                json.dump(ast_data, f)

    def tearDown(self):
        """Clean up the mock environment."""
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_classify_repository_script(self):
        """Test the end-to-end functionality of the classify_repository.py script."""
        script_path = "tooling/classify_repository.py"
        command = [
            "python3", script_path,
            "--ast-dir", self.ast_dir,
            "--output-file", self.output_file
        ]

        # Run the script
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Script failed with error: {result.stderr}")

        # Verify the output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Verify the content of the report
        with open(self.output_file, "r") as f:
            report = json.load(f)

        expected_report = {
            "regular.py": "REGULAR (TYPE-3)",
            "context_free.py": "CONTEXT-FREE (TYPE-2)"
        }
        self.assertEqual(report, expected_report)

if __name__ == "__main__":
    unittest.main()
