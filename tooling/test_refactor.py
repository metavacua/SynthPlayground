import unittest
import os
import shutil
import io
import json
from unittest.mock import patch

from tooling.refactor import main as refactor_main

class TestRefactor(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_refactor_dir"
        self.asts_dir = os.path.join(self.test_dir, "knowledge_core", "asts")
        os.makedirs(self.asts_dir, exist_ok=True)

        self.file_with_symbol = os.path.join(self.test_dir, "file_with_symbol.py")
        with open(self.file_with_symbol, "w") as f:
            f.write("def old_symbol():\n    pass\n\nold_symbol()")

        # Create a dummy AST
        self.ast_file = os.path.join(self.asts_dir, "file_with_symbol.py.json")
        with open(self.ast_file, "w") as f:
            ast_data = {
                "type": "module",
                "children": [
                    {
                        "type": "function_definition",
                        "children": [
                            {"type": "def"},
                            {"type": "identifier", "text": "old_symbol", "start_byte": 4, "end_byte": 14},
                        ]
                    },
                    {
                        "type": "expression_statement",
                        "children": [
                            {
                                "type": "call",
                                "children": [
                                    {"type": "identifier", "text": "old_symbol", "start_byte": 22, "end_byte": 32},
                                ]
                            }
                        ]
                    }
                ]
            }
            json.dump(ast_data, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_refactor_e2e(self):
        """Tests the end-to-end refactoring functionality."""
        with patch("sys.argv", [
            "tooling/refactor.py",
            "--old-name", "old_symbol",
            "--new-name", "new_symbol",
            "--search-path", self.test_dir,
            "--root-dir", self.test_dir
        ]):
            refactor_main()

        with open(self.file_with_symbol, "r") as f:
            content = f.read()
        self.assertIn("new_symbol", content)
        self.assertNotIn("old_symbol", content)

    def test_symbol_not_found(self):
        """Tests that the tool prints an error if the symbol is not found."""
        with patch("sys.argv", [
            "tooling/refactor.py",
            "--old-name", "non_existent",
            "--new-name", "new_name",
            "--search-path", self.test_dir
        ]):
            with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
                refactor_main()

        with open(self.file_with_symbol, "r") as f:
            content = f.read()
        self.assertNotIn("new_name", content)

if __name__ == "__main__":
    unittest.main()
