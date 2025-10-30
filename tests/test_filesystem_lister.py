import unittest
import os
import shutil
import sys
import tempfile

# Add root directory for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.filesystem_lister import list_all_files_and_dirs

class TestFilesystemLister(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory structure for testing."""
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, "empty_subdir"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "subdir_with_file"), exist_ok=True)
        with open(os.path.join(self.test_dir, "subdir_with_file", "a.txt"), "w") as f:
            f.write("test")
        with open(os.path.join(self.test_dir, "root.txt"), "w") as f:
            f.write("root")

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_lists_all_items(self):
        """Verify that all files and directories are listed correctly."""
        # The function returns paths relative to the given root_dir.
        result_paths = list_all_files_and_dirs(self.test_dir)

        expected_relative_paths = sorted([
            './',
            'empty_subdir/',
            'root.txt',
            'subdir_with_file/',
            'subdir_with_file/a.txt'
        ])

        self.assertEqual(result_paths, expected_relative_paths)

if __name__ == "__main__":
    unittest.main()
