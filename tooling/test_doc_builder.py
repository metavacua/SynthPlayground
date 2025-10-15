import unittest
import os
import json
from unittest.mock import patch
from tooling.doc_builder import generate_system_docs, generate_readme, generate_pages

class TestUnifiedDocBuilder(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_doc_builder_dir"
        os.makedirs(os.path.join(self.test_dir, "tooling"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "knowledge_core"), exist_ok=True)

        self.py_file = os.path.join(self.test_dir, "tooling", "sample_tool.py")
        self.agents_md = os.path.join(self.test_dir, "AGENTS.md")
        self.readme_md = os.path.join(self.test_dir, "README.md")
        self.system_docs = os.path.join(self.test_dir, "knowledge_core", "SYSTEM_DOCS.md")
        self.index_html = os.path.join(self.test_dir, "index.html")

        with open(self.py_file, "w") as f:
            f.write('"""This is a sample tool."""\ndef sample_function():\n    """A sample function."""\n    pass')
        with open(self.agents_md, "w") as f:
            f.write("```json\n{\"protocol_id\": \"sample-proto-001\", \"description\": \"A sample protocol.\"}\n```")
        with open(self.readme_md, "w") as f: # Pre-create for pages test
            f.write("# Sample Readme")


    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    @patch('tooling.doc_builder.ROOT_DIR', new_callable=lambda: os.getcwd() + '/test_doc_builder_dir')
    def test_generate_system_docs(self, mock_root):
        generate_system_docs([os.path.join(self.test_dir, "tooling")], self.system_docs)
        self.assertTrue(os.path.exists(self.system_docs))
        with open(self.system_docs, "r") as f:
            content = f.read()
        self.assertIn("## `test_doc_builder_dir/tooling/` Directory", content)
        self.assertIn("This is a sample tool.", content)

    @patch('tooling.doc_builder.ROOT_DIR', new_callable=lambda: os.getcwd())
    def test_generate_readme(self, mock_root):
        generate_readme(self.agents_md, self.readme_md)
        self.assertTrue(os.path.exists(self.readme_md))
        with open(self.readme_md, "r") as f:
            content = f.read()
        self.assertIn("sample-proto-001", content)
        self.assertIn("sample_tool.py", content)

    def test_generate_pages(self):
        generate_pages(self.readme_md, self.agents_md, self.index_html)
        self.assertTrue(os.path.exists(self.index_html))
        with open(self.index_html, "r") as f:
            content = f.read()
        self.assertIn("<h1>README</h1>", content)
        self.assertIn("<h1>AGENTS.md</h1>", content)


if __name__ == "__main__":
    unittest.main()