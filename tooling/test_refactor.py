import unittest
import os
import shutil
from unittest.mock import patch
from tooling.refactor import (
    find_symbol_definition,
    find_references,
    main as refactor_main,
)


class TestRefactor(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_refactor_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_with_symbol = os.path.join(self.test_dir, "file_with_symbol.py")
        self.referencing_file = os.path.join(self.test_dir, "referencing_file.py")

        with open(self.file_with_symbol, "w") as f:
            f.write("def old_name():\n    pass")

        with open(self.referencing_file, "w") as f:
            f.write("from file_with_symbol import old_name\n\nold_name()")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_symbol_definition(self):
        """Tests finding a symbol's definition."""
        node = find_symbol_definition(self.file_with_symbol, "old_name")
        self.assertIsNotNone(node)
        self.assertEqual(node.name, "old_name")

    def test_find_references(self):
        """Tests finding references to a symbol."""
        references = find_references("old_name", self.test_dir)
        self.assertEqual(len(references), 2)
        self.assertIn(self.file_with_symbol, references)
        self.assertIn(self.referencing_file, references)

    @patch(
        "sys.argv",
        new_callable=lambda: [
            "tooling/refactor.py",
            "--filepath",
            "test_refactor_dir/file_with_symbol.py",
            "--old-name",
            "old_name",
            "--new-name",
            "new_name",
            "--search-path",
            "test_refactor_dir",
        ],
    )
    @patch("builtins.print")
    def test_main_plan_generation(self, mock_print, mock_argv):
        """Tests that the main function generates a correct refactoring plan."""
        refactor_main()

        # Check that a plan file path was printed to stdout
        mock_print.assert_called_once()
        plan_path = mock_print.call_args[0][0]
        self.assertTrue(os.path.exists(plan_path))

        with open(plan_path, "r") as f:
            content = f.read()

        self.assertIn(f"replace_with_git_merge_diff\n{self.file_with_symbol}", content)
        self.assertIn(f"replace_with_git_merge_diff\n{self.referencing_file}", content)

        os.remove(plan_path)

    def test_symbol_not_found(self):
        """Tests that the tool exits if the symbol is not found."""
        with patch(
            "sys.argv",
            [
                "tooling/refactor.py",
                "--filepath",
                self.file_with_symbol,
                "--old-name",
                "non_existent",
                "--new-name",
                "new_name",
            ],
        ):
            with self.assertRaises(SystemExit):
                refactor_main()


if __name__ == "__main__":
    unittest.main()
