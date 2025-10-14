import os
import subprocess
import unittest
import tempfile
import shutil


class TestRefactorTool(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for our test files
        self.test_dir = tempfile.mkdtemp()
        self.file_to_refactor = os.path.join(self.test_dir, "file1.py")
        self.referencing_file = os.path.join(self.test_dir, "file2.py")

        with open(self.file_to_refactor, "w") as f:
            f.write("def old_function_name():\n")
            f.write("    pass\n")

        with open(self.referencing_file, "w") as f:
            f.write("from file1 import old_function_name\n")
            f.write("\n")
            f.write("old_function_name()\n")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_rename_symbol(self):
        # Run the refactor tool
        result = subprocess.run(
            [
                "python",
                "tooling/refactor.py",
                "--filepath",
                self.file_to_refactor,
                "--old-name",
                "old_function_name",
                "--new-name",
                "new_function_name",
                "--search-path",
                self.test_dir,
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        plan_path = result.stdout.strip()
        self.assertTrue(os.path.exists(plan_path))

        # Check the content of the generated plan
        with open(plan_path, "r") as f:
            plan_content = f.read()

        # The plan should contain two replace_with_git_merge_diff blocks
        self.assertIn(
            f"replace_with_git_merge_diff\n{self.file_to_refactor}", plan_content
        )
        self.assertIn(
            f"replace_with_git_merge_diff\n{self.referencing_file}", plan_content
        )
        self.assertIn("def new_function_name():", plan_content)
        self.assertIn("from file1 import new_function_name", plan_content)

        # Clean up the plan file
        os.remove(plan_path)


if __name__ == "__main__":
    unittest.main()
