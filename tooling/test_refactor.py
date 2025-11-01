import os
import shutil
import unittest
from unittest.mock import patch
from tooling.refactor import main as refactor_main, find_references


class TestRefactor(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory and files for testing."""
        self.test_dir = "test_refactor_dir"
        self.ast_dir = os.path.join(self.test_dir, "knowledge_core", "asts")
        os.makedirs(self.ast_dir, exist_ok=True)

        self.file_with_symbol = os.path.join(self.test_dir, "file_with_symbol.py")
        self.file_with_reference = os.path.join(
            self.test_dir, "file_with_reference.py"
        )

        # Create dummy source files
        with open(self.file_with_symbol, "w") as f:
            f.write("def old_name():\n    pass\n")
        with open(self.file_with_reference, "w") as f:
            f.write("from file_with_symbol import old_name\nold_name()\n")

        # Create corresponding dummy ASTs
        self.ast_symbol = os.path.join(self.ast_dir, "file_with_symbol.py.json")
        self.ast_reference = os.path.join(
            self.ast_dir, "file_with_reference.py.json"
        )

        ast_symbol_content = {
            "type": "module",
            "children": [
                {
                    "type": "function_definition",
                    "children": [
                        {"type": "def", "text": "def"},
                        {
                            "type": "identifier",
                            "text": "old_name",
                            "start_byte": 4,
                            "end_byte": 12,
                        },
                    ],
                }
            ],
        }
        ast_reference_content = {
            "type": "module",
            "children": [
                {
                    "type": "import_from_statement",
                    "children": [
                        {
                            "type": "identifier",
                            "text": "old_name",
                            "start_byte": 29,
                            "end_byte": 37,
                        }
                    ],
                },
                {
                    "type": "call",
                    "children": [
                        {
                            "type": "identifier",
                            "text": "old_name",
                            "start_byte": 38,
                            "end_byte": 46,
                        }
                    ],
                },
            ],
        }

        with open(self.ast_symbol, "w") as f:
            f.write(str(ast_symbol_content).replace("'", '"'))
        with open(self.ast_reference, "w") as f:
            f.write(str(ast_reference_content).replace("'", '"'))

    def tearDown(self):
        """Clean up the temporary directory and files."""
        shutil.rmtree(self.test_dir)

    def test_refactor_e2e(self):
        """An end-to-end test to ensure the refactor tool works as expected."""
        with patch(
            "sys.argv",
            [
                "tooling/refactor.py",
                "--old-name",
                "old_name",
                "--new-name",
                "new_name",
                "--search-path",
                self.test_dir,
                "--root-dir",
                self.test_dir,
            ],
        ):
            refactor_main()

        with open(self.file_with_symbol, "r") as f:
            content = f.read()
            self.assertNotIn("old_name", content)
            self.assertIn("new_name", content)
        with open(self.file_with_reference, "r") as f:
            content = f.read()
            self.assertNotIn("old_name", content)
            self.assertIn("new_name", content)


if __name__ == "__main__":
    unittest.main()
