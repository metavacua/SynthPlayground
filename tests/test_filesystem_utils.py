import unittest
import os
import shutil
import sys

# Add root directory for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.filesystem_utils import find_files

class TestFileSystemUtils(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = "temp_test_fs_utils"
        # Create a nested structure
        self.nested_dir = os.path.join(self.test_dir, "nested")
        self.ignored_dir = os.path.join(self.test_dir, "archive") # Matches default ignore
        os.makedirs(self.nested_dir, exist_ok=True)
        os.makedirs(self.ignored_dir, exist_ok=True)

        # Create test files
        with open(os.path.join(self.test_dir, "a.txt"), "w") as f:
            f.write("a")
        with open(os.path.join(self.nested_dir, "b.txt"), "w") as f:
            f.write("b")
        with open(os.path.join(self.test_dir, "c.log"), "w") as f: # Should be ignored
            f.write("c")
        with open(os.path.join(self.ignored_dir, "d.txt"), "w") as f: # Should be ignored
            f.write("d")

        # Create a custom ignore file
        self.ignore_file = os.path.join(self.test_dir, ".myignore")
        with open(self.ignore_file, "w") as f:
            f.write("*.log\n")
            f.write("b.txt\n")
            f.write("nested/\n")

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_find_files_recursively(self):
        """Test basic recursive file finding."""
        found = find_files(self.test_dir)
        expected = [
            os.path.abspath(os.path.join(self.test_dir, ".myignore")),
            os.path.abspath(os.path.join(self.test_dir, "a.txt")),
            os.path.abspath(os.path.join(self.nested_dir, "b.txt")),
        ]
        # With pathspec, we don't need to worry about default ignores as much
        # as it should handle them correctly.
        found_files = find_files(self.test_dir, ignore_patterns=[".myignore"])
        expected = [os.path.abspath(os.path.join(self.test_dir, "a.txt")),
                    os.path.abspath(os.path.join(self.nested_dir, "b.txt"))]
        self.assertEqual(sorted(found_files), sorted(expected))


    def test_find_files_non_recursively(self):
        """Test non-recursive file finding."""
        found = find_files(self.test_dir, recursive=False, ignore_patterns=[".myignore"])
        expected = [os.path.abspath(os.path.join(self.test_dir, "a.txt"))]
        self.assertEqual(found, expected)

    def test_find_files_with_search_pattern(self):
        """Test finding files that match a specific pattern."""
        found = find_files(self.test_dir, search_patterns=["a.*"], ignore_patterns=[".myignore"])
        expected = [os.path.abspath(os.path.join(self.test_dir, "a.txt"))]
        self.assertEqual(found, expected)

    def test_default_ignore_patterns(self):
        """Test that default ignore patterns (e.g., for .log, archive/) are applied."""
        found = find_files(self.test_dir, ignore_patterns=[".myignore"])
        self.assertNotIn(os.path.abspath(os.path.join(self.test_dir, "c.log")), found)
        self.assertNotIn(os.path.abspath(os.path.join(self.ignored_dir, "d.txt")), found)

    def test_custom_ignore_file(self):
        """Test that a custom ignore file is correctly used."""
        found = find_files(self.test_dir, ignore_file_path=self.ignore_file)
        expected = [os.path.abspath(os.path.join(self.test_dir, "a.txt"))]
        self.assertEqual(found, expected)

    def test_additional_ignore_patterns(self):
        """Test that additional, ad-hoc ignore patterns can be supplied."""
        found = find_files(self.test_dir, ignore_patterns=["a.txt", ".myignore"])
        expected = [os.path.abspath(os.path.join(self.nested_dir, "b.txt"))]
        self.assertEqual(found, expected)

    def test_non_existent_start_dir(self):
        """Test that the function handles a non-existent start directory gracefully."""
        found = find_files("non_existent_dir_abc")
        self.assertEqual(found, [])

if __name__ == "__main__":
    unittest.main()