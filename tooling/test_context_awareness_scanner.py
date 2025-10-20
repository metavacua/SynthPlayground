import unittest
import os
import json
import shutil
from unittest.mock import patch
from tooling.context_awareness_scanner import (
    get_defined_symbols,
    get_imported_symbols,
    find_references,
    main as scanner_main,
)


class TestContextAwarenessScanner(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_context_scanner_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_to_scan = os.path.join(self.test_dir, "file_to_scan.py")
        self.referencing_file = os.path.join(self.test_dir, "referencing_file.py")

        with open(self.file_to_scan, "w") as f:
            f.write(
                "import os\nfrom my_module import another_func\n\nclass MyClass:\n    pass\n\ndef my_func():\n    pass"
            )

        with open(self.referencing_file, "w") as f:
            f.write("from file_to_scan import my_func\n\nmy_func()")

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        report_file = f"{os.path.basename(self.file_to_scan)}.json"
        if os.path.exists(report_file):
            os.remove(report_file)

    def test_get_defined_symbols(self):
        """Tests the extraction of defined functions and classes."""
        symbols = get_defined_symbols(self.file_to_scan)
        self.assertEqual(len(symbols), 2)
        self.assertEqual(symbols[0]["name"], "MyClass")
        self.assertEqual(symbols[1]["name"], "my_func")

    def test_get_imported_symbols(self):
        """Tests the extraction of imported symbols."""
        imports = get_imported_symbols(self.file_to_scan)
        self.assertEqual(len(imports), 2)
        self.assertEqual(imports[0]["name"], "os")
        self.assertEqual(imports[1]["name"], "my_module.another_func")

    def test_find_references(self):
        """Tests finding references to a symbol."""
        references = find_references("my_func", self.test_dir)
        self.assertEqual(len(references), 2)  # Should be found in both files
        self.assertIn(self.file_to_scan, references)
        self.assertIn(self.referencing_file, references)

    @patch(
        "sys.argv",
        new_callable=lambda: [
            "tooling/context_awareness_scanner.py",
            "test_context_scanner_dir/file_to_scan.py",
            "--search-path",
            "test_context_scanner_dir",
        ],
    )
    def test_main_report_generation(self, mock_argv):
        """Tests that the main function generates a correct JSON report."""
        scanner_main()

        report_file = f"{os.path.basename(self.file_to_scan)}.json"
        self.assertTrue(os.path.exists(report_file))

        with open(report_file, "r") as f:
            report = json.load(f)

        self.assertEqual(report["file_path"], self.file_to_scan)
        self.assertEqual(len(report["defined_symbols"]), 2)
        self.assertEqual(len(report["imported_symbols"]), 2)
        self.assertEqual(len(report["defined_symbols"][1]["references"]), 2)


if __name__ == "__main__":
    unittest.main()
