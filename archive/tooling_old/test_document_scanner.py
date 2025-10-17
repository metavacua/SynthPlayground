import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from tooling.document_scanner import scan_documents
import pypdf

class TestDocumentScanner(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_document_scanner_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.md_file = os.path.join(self.test_dir, "test.md")
        self.txt_file = os.path.join(self.test_dir, "test.txt")
        self.pdf_file = os.path.join(self.test_dir, "test.pdf")

        with open(self.md_file, "w") as f:
            f.write("# Markdown Content")
        with open(self.txt_file, "w") as f:
            f.write("Text Content")
        # Create a dummy PDF file
        with open(self.pdf_file, "w") as f:
            f.write("dummy pdf content")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_md_and_txt_files(self):
        """Tests that the scanner correctly reads .md and .txt files."""
        scanned_data = scan_documents(self.test_dir)
        self.assertIn(self.md_file, scanned_data)
        self.assertEqual(scanned_data[self.md_file], "# Markdown Content")
        self.assertIn(self.txt_file, scanned_data)
        self.assertEqual(scanned_data[self.txt_file], "Text Content")

    @patch('tooling.document_scanner.PdfReader')
    def test_scan_pdf_file(self, mock_pdf_reader):
        """Tests that the scanner correctly reads .pdf files."""
        # Mock the PdfReader to return a dummy page with text
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "PDF Content"
        mock_pdf_reader.return_value.pages = [mock_page]

        scanned_data = scan_documents(self.test_dir)

        self.assertIn(self.pdf_file, scanned_data)
        self.assertEqual(scanned_data[self.pdf_file], "PDF Content")

    @patch('builtins.open', side_effect=IOError("Read error"))
    def test_read_error_handling(self, mock_open):
        """Tests that the scanner handles file read errors gracefully."""
        scanned_data = scan_documents(self.test_dir)
        # The scanner should still return a result, but with an error message
        self.assertTrue(any("Error reading file" in v for v in scanned_data.values()))

if __name__ == "__main__":
    unittest.main()