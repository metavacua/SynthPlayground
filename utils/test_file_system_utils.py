import unittest
import os
import tempfile
import shutil
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.file_system_utils import find_files, ROOT_DIR


class TestFileSystemUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

        # Create a dummy .julesignore file
        with open(".julesignore", "w") as f:
            f.write("*.log\n")
            f.write("ignored_dir/\n")

        # Create some dummy files and directories
        os.makedirs("app/data")
        os.makedirs("ignored_dir")
        with open("app/data/file1.txt", "w") as f:
            f.write("test")
        with open("app/file2.txt", "w") as f:
            f.write("test")
        with open("app/data/file.log", "w") as f:
            f.write("test")
        with open("ignored_dir/file3.txt", "w") as f:
            f.write("test")

    def tearDown(self):
        os.chdir(ROOT_DIR)
        shutil.rmtree(self.test_dir)

    def test_find_files(self):
        # Find all .txt files
        txt_files = find_files("*.txt", base_dir=".")
        self.assertEqual(len(txt_files), 2)
        self.assertIn("app/data/file1.txt", txt_files)
        self.assertIn("app/file2.txt", txt_files)

        # Make sure log files are ignored
        log_files = find_files("*.log", base_dir=".")
        self.assertEqual(len(log_files), 0)

        # Make sure ignored directories are ignored
        self.assertNotIn("ignored_dir/file3.txt", txt_files)


if __name__ == "__main__":
    unittest.main()
