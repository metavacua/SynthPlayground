import os
import shutil
import unittest
from tooling.build_protocol import build_protocol

class TestBuildProtocol(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test environment."""
        self.source_dir = "test_protocol_sources"
        self.output_file = "TEST_AGENTS.md"
        os.makedirs(self.source_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_build_protocol_concatenates_in_order(self):
        """
        Tests that the script correctly concatenates sorted markdown files.
        """
        # Create dummy source files
        with open(os.path.join(self.source_dir, "01_part_b.md"), "w") as f:
            f.write("Content B")
        with open(os.path.join(self.source_dir, "00_part_a.md"), "w") as f:
            f.write("Content A")

        # Run the build script with test-specific paths
        build_protocol(source_dir=self.source_dir, output_file=self.output_file)

        # Check if the output file was created and has the correct content
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r") as f:
            content = f.read()
            expected_content = "Content A\n\nContent B"
            self.assertEqual(content, expected_content)

    def test_no_markdown_files(self):
        """
        Tests that the script handles cases with no markdown files gracefully.
        """
        # Run the build script in an empty directory
        build_protocol(source_dir=self.source_dir, output_file=self.output_file)
        # The script should not create an output file
        self.assertFalse(os.path.exists(self.output_file))

if __name__ == "__main__":
    unittest.main()