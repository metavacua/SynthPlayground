import unittest
import os
import tempfile
import shutil
from unittest.mock import patch

from tooling import readme_generator


class TestReadmeGenerator(unittest.TestCase):
    """
    Tests for the readme_generator.py script.
    """

    def setUp(self):
        """
        Set up a temporary directory and mock source files for testing.
        """
        self.test_dir = tempfile.mkdtemp()
        self.tooling_dir = os.path.join(self.test_dir, "tooling")
        os.makedirs(self.tooling_dir)

        # Create dummy files with docstrings to be parsed
        self.mock_files_info = {
            "component_one.py": '"""This is the first component."""',
            "component_two.py": '"""This is the second component.\\n\\nIt has multiple lines."""',
            "component_three.py": "# No docstring here",
        }

        for name, content in self.mock_files_info.items():
            with open(os.path.join(self.tooling_dir, name), "w") as f:
                f.write(content)

    def tearDown(self):
        """
        Clean up the temporary directory after tests are complete.
        """
        shutil.rmtree(self.test_dir)

    def test_generate_key_components_section(self):
        """
        Verify that the key components section is generated correctly from mock files.
        """
        files_to_doc = ["component_one.py", "component_two.py"]
        # Patch the constants to point to our test setup
        with patch(
            "tooling.readme_generator.KEY_COMPONENTS_DIR", self.tooling_dir
        ), patch("tooling.readme_generator.KEY_FILES_TO_DOCUMENT", files_to_doc):

            result = readme_generator.generate_key_components_section()

        # The path in the output will be the full temporary path.
        path_one = os.path.join(self.tooling_dir, "component_one.py")
        self.assertIn(f"- **`{path_one}`**:", result)
        self.assertIn("> This is the first component.", result)

        path_two = os.path.join(self.tooling_dir, "component_two.py")
        self.assertIn(f"- **`{path_two}`**:", result)
        self.assertIn("> This is the second component.", result)
        self.assertIn("> It has multiple lines.", result)

        self.assertNotIn("component_three.py", result)

    def test_main_generates_readme_correctly(self):
        """
        Test the main function to ensure it generates a complete README.md.
        """
        output_filepath = os.path.join(self.test_dir, "TEST_README.md")
        key_files = ["component_one.py", "component_two.py", "component_three.py"]

        # Patch the configuration constants within the readme_generator module
        with patch("tooling.readme_generator.OUTPUT_FILE", output_filepath), patch(
            "tooling.readme_generator.KEY_FILES_TO_DOCUMENT", key_files
        ), patch("tooling.readme_generator.KEY_COMPONENTS_DIR", self.tooling_dir):

            readme_generator.main()

        # Verify the output file was created
        self.assertTrue(os.path.exists(output_filepath))

        # Verify the content of the generated file
        with open(output_filepath, "r") as f:
            content = f.read()

        # Check for static content
        self.assertIn("# Project Chimera", content)
        self.assertIn("## Build System & Usage", content)

        # Check for dynamically generated content
        path_one = os.path.join(self.tooling_dir, "component_one.py")
        self.assertIn(f"`{path_one}`", content)
        self.assertIn("> This is the first component.", content)

        # Check that the component without a docstring is handled gracefully
        path_three = os.path.join(self.tooling_dir, "component_three.py")
        self.assertIn(f"`{path_three}`", content)
        self.assertIn("> _No docstring found._", content)


if __name__ == "__main__":
    unittest.main()
