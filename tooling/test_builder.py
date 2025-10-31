import unittest
import os
import yaml
import shutil
from unittest.mock import patch, call
from tooling.builder import main as builder_main, execute_build

class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_builder_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.build_config = {
            "targets": {
                "compile": {
                    "type": "compiler",
                    "description": "A test compiler.",
                    "compiler": "tooling/compiler.py",
                    "command": "python3 {compiler} --source-dir {source} --output-file {output}",
                    "output": "output/all.md",
                    "sources": ["sources/"],
                },
                "test": {
                    "type": "command",
                    "description": "A test command.",
                    "command": "python -m unittest discover tests/",
                },
            },
            "build_groups": {"all": ["compile", "test"]},
        }
        patcher = patch("yaml.safe_load", return_value=self.build_config)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("tooling.builder.subprocess.run")
    def test_execute_compiler_target(self, mock_run):
        execute_build("compile", self.build_config, [])
        mock_run.assert_called_once()
        expected_command = "python3 {} --source-dir {} --output-file {}".format(
            os.path.join(os.getcwd(), "tooling/compiler.py"),
            os.path.join(os.getcwd(), "sources/"),
            os.path.join(os.getcwd(), "output/all.md"),
        ).split()
        self.assertEqual(mock_run.call_args[0][0], expected_command)

    @patch("tooling.builder.subprocess.run")
    def test_execute_command_target(self, mock_run):
        execute_build("test", self.build_config, [])
        mock_run.assert_called_once_with(
            "python -m unittest discover tests/",
            check=True,
            capture_output=True,
            text=True,
            shell=True,
            cwd=os.getcwd(),
        )

    @patch("tooling.builder.execute_build")
    def test_build_group_execution(self, mock_execute_build):
        with patch("sys.argv", ["tooling/builder.py", "--target", "all"]):
            builder_main()
        calls = [call("compile", self.build_config, []), call("test", self.build_config, [])]
        mock_execute_build.assert_has_calls(calls, any_order=False)

    def test_invalid_target(self):
        with self.assertRaises(ValueError):
            execute_build("invalid", self.build_config, [])

if __name__ == "__main__":
    unittest.main()
