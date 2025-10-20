import unittest
import os
import shutil
import json
from tooling.doc_builder import generate_system_docs, generate_readme, generate_pages


class TestDocBuilder(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_doc_builder_dir"
        os.makedirs(os.path.join(self.test_dir, "tooling"), exist_ok=True)
        # No longer creating a separate output dir, as the builder expects a certain structure
        # os.makedirs(os.path.join(self.test_dir, "output"), exist_ok=True)

        # Create a sample Python file for system doc generation
        self.py_file_path = os.path.join(self.test_dir, "tooling", "sample_tool.py")
        with open(self.py_file_path, "w") as f:
            f.write(
                '"""This is a sample tool."""\n\ndef sample_function():\n    """This is a sample function."""\n    pass'
            )

        # Create a sample AGENTS.md for README generation
        self.agents_md_path = os.path.join(self.test_dir, "AGENTS.md")
        with open(self.agents_md_path, "w") as f:
            f.write(
                '```json\n{"protocol_id": "DOC-001", "description": "A test protocol."}\n```'
            )

        # Create a dummy README.md for pages generation
        self.readme_path = os.path.join(self.test_dir, "README.md")
        with open(self.readme_path, "w") as f:
            f.write("# Test README")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_system_docs(self):
        """Tests the generation of system documentation from Python files."""
        output_file = os.path.join(self.test_dir, "SYSTEM.md")
        generate_system_docs(
            source_dirs=[os.path.join(self.test_dir, "tooling")],
            output_file=output_file,
        )

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn(f"### `/app/{self.test_dir}/tooling/sample_tool.py`", content)
        self.assertIn("This is a sample tool.", content)
        self.assertIn("`def sample_function()`", content)
        self.assertIn("This is a sample function.", content)

    def test_generate_readme(self):
        """Tests the generation of a README.md from an AGENTS.md file."""
        # The output file needs to be in the root of the test dir for tooling/ to be found
        output_file = os.path.join(self.test_dir, "README.md")
        generate_readme(agents_md_path=self.agents_md_path, output_file=output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn("## Core Protocols", content)
        self.assertIn("- **`DOC-001`**: A test protocol.", content)
        self.assertIn("## Key Components", content)
        self.assertIn("- **`tooling/sample_tool.py`**", content)
        self.assertIn("This is a sample tool.", content)

    def test_generate_pages(self):
        """Tests the generation of a GitHub Pages index.html file."""
        output_file = os.path.join(self.test_dir, "index.html")
        generate_pages(
            readme_path=self.readme_path,
            agents_md_path=self.agents_md_path,
            output_file=output_file,
        )

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn("<h1>README</h1>", content)
        # Corrected assertion: markdown converts '# title' to '<h1>title</h1>'
        self.assertIn("<h1>Test README</h1>", content)
        self.assertIn("<h1>AGENTS.md</h1>", content)
        self.assertIn("DOC-001", content)

    def test_generate_readme_missing_agents_md(self):
        """Tests that README generation handles a missing AGENTS.md file."""
        output_file = os.path.join(self.test_dir, "README_NO_AGENTS.md")
        generate_readme(
            agents_md_path="non_existent_agents.md", output_file=output_file
        )

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn("_Error: `non_existent_agents.md` not found._", content)

    def test_system_docs_no_docstring(self):
        """Tests that system docs correctly report missing docstrings."""
        # Create a Python file with no module-level docstring
        py_file_no_docstring = os.path.join(self.test_dir, "tooling", "no_docstring.py")
        with open(py_file_no_docstring, "w") as f:
            f.write("def my_func():\n    pass")

        output_file = os.path.join(self.test_dir, "SYSTEM_NO_DOC.md")
        generate_system_docs(
            source_dirs=[os.path.join(self.test_dir, "tooling")],
            output_file=output_file,
        )

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r") as f:
            content = f.read()

        self.assertIn(f"### `/app/{self.test_dir}/tooling/no_docstring.py`", content)
        self.assertIn("_No module-level docstring found._", content)


if __name__ == "__main__":
    unittest.main()
