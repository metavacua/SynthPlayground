import unittest
import os
import json
import shutil
from unittest.mock import patch, call
from tooling.builder import main as builder_main, execute_build


class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_builder_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_path = os.path.join(self.test_dir, "build_config.json")
        self.build_config = {
            "targets": {
                "compile": {
                    "type": "compiler",
                    "compiler": "tooling/compiler.py",
                    "output": "output/all.md",
                    "sources": ["sources/"],
                },
                "test": {
                    "type": "command",
                    "command": "python -m unittest discover tests/",
                },
            },
            "build_groups": {"all": ["compile", "test"]},
        }
        with open(self.config_path, "w") as f:
            json.dump(self.build_config, f)

        # Patch the CONFIG_FILE path to use our temporary file
        patcher = patch("tooling.builder.CONFIG_FILE", self.config_path)
        patcher.start()
        self.addCleanup(patcher.stop)

        # Patch ROOT_DIR to be our test_dir
        patcher_root = patch("tooling.builder.ROOT_DIR", self.test_dir)
        patcher_root.start()
        self.addCleanup(patcher_root.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("tooling.builder.subprocess.run")
    def test_execute_compiler_target(self, mock_run):
        """Tests execution of a compiler target."""
        execute_build("compile", self.build_config)
        mock_run.assert_called_once()
        # Check that the command was constructed correctly
        expected_command = [
            "python3",
            os.path.join(self.test_dir, "tooling/compiler.py"),
            "--source-dir",
            os.path.join(self.test_dir, "sources/"),
            "--output-file",
            os.path.join(self.test_dir, "output/all.md"),
        ]
        self.assertEqual(mock_run.call_args[0][0], expected_command)

    @patch("tooling.builder.subprocess.run")
    def test_execute_command_target(self, mock_run):
        """Tests execution of a command target."""
        execute_build("test", self.build_config)
        mock_run.assert_called_once_with(
            "python -m unittest discover tests/",
            check=True,
            capture_output=True,
            text=True,
            cwd=self.test_dir,
            shell=True,
        )

    @patch("tooling.builder.execute_build")
    def test_build_group_execution(self, mock_execute_build):
        """Tests that a build group executes its targets in order."""
        with patch("sys.argv", ["tooling/builder.py", "--target", "all"]):
            builder_main()

        calls = [call("compile", self.build_config), call("test", self.build_config)]
        mock_execute_build.assert_has_calls(calls, any_order=False)

    def test_invalid_target(self):
        """Tests that the builder exits on an invalid target name."""
        with self.assertRaises(ValueError):
            execute_build("invalid", self.build_config)


if __name__ == "__main__":
    unittest.main()
