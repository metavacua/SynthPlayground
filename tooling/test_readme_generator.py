import unittest
import os
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock

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

        # Create a dummy AGENTS.md
        self.agents_md_path = os.path.join(self.test_dir, "AGENTS.md")
        with open(self.agents_md_path, "w") as f:
            f.write("""
# Test Agents MD

```json
{
  "protocol_id": "test-proto-1",
  "description": "This is a test protocol."
}
```

## Child Module: `child`

This module contains the following protocols, which are defined in its own `AGENTS.md` file:

- `child-proto-1`

---
            """)

    def tearDown(self):
        """
        Clean up the temporary directory after tests are complete.
        """
        shutil.rmtree(self.test_dir)

    def test_main_generates_readme_correctly(self):
        """
        Test the main function to ensure it generates a complete README.md
        by simulating command-line arguments.
        """
        output_filepath = os.path.join(self.test_dir, "TEST_README.md")

        # Mock sys.argv to simulate command-line execution
        test_args = [
            "readme_generator.py",
            "--source-file", self.agents_md_path,
            "--output-file", output_filepath
        ]

        readme_generator.main(self.agents_md_path, output_filepath)

        # Verify the output file was created
        self.assertTrue(os.path.exists(output_filepath))

        # Verify the content of the generated file
        with open(output_filepath, "r") as f:
            content = f.read()

        # Check for static content
        self.assertIn("# Module Documentation", content)
        self.assertIn("## Core Protocols", content)

        # Check for protocol content from AGENTS.md
        self.assertIn("- **`test-proto-1`**: This is a test protocol.", content)

        # Check for child module summary
        self.assertIn("### Child Module: `child`", content)
        self.assertIn("- `child-proto-1`", content)

        # Check for key component docstrings
        self.assertIn("## Key Components", content)
        self.assertIn("- **`tooling/component_one.py`**:", content)
        self.assertIn("> This is the first component.", content)
        self.assertIn("- **`tooling/component_two.py`**:", content)
        self.assertIn("> This is the second component.", content)
        self.assertIn("- **`tooling/component_three.py`**:", content)
        self.assertIn("> _No docstring found._", content)

if __name__ == "__main__":
    unittest.main()