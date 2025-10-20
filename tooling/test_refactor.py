import os
import io
import unittest
from unittest.mock import patch
from tooling.refactor import main as refactor_main


class TestRefactor(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory and files for testing."""
        self.test_dir = "test_refactor_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_with_symbol = os.path.join(self.test_dir, "file_with_symbol.py")
        self.file_with_reference = os.path.join(self.test_dir, "file_with_reference.py")

        with open(self.file_with_symbol, "w") as f:
            f.write("def old_name():\n    pass\n")
        with open(self.file_with_reference, "w") as f:
            f.write("from file_with_symbol import old_name\nold_name()\n")

    def tearDown(self):
        """Clean up the temporary directory and files."""
        if os.path.exists(self.file_with_symbol):
            os.remove(self.file_with_symbol)
        if os.path.exists(self.file_with_reference):
            os.remove(self.file_with_reference)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_refactor_e2e(self):
        """An end-to-end test to ensure the refactor tool works as expected."""
        with patch(
            "sys.argv",
            [
                "tooling/refactor.py",
                "--filepath",
                self.file_with_symbol,
                "--old-name",
                "old_name",
                "--new-name",
                "new_name",
                "--search-path",
                self.test_dir,
            ],
        ):
            refactor_main()

        with open(self.file_with_symbol, "r") as f:
            self.assertIn("new_name", f.read())
        with open(self.file_with_reference, "r") as f:
            self.assertIn("new_name", f.read())

    def test_symbol_not_found(self):
        """Tests that the tool prints an error if the symbol is not found."""
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
            with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
                refactor_main()
                self.assertEqual(
                    mock_stderr.getvalue(),
                    f"Error: Symbol 'non_existent' not found in {self.file_with_symbol}\n"
                )


if __name__ == "__main__":
    unittest.main()
