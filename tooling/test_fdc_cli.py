import unittest
import os
import json
import shutil
from unittest.mock import patch
from tooling.fdc_cli import main as fdc_main


class TestFdcCli(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_fdc_cli_dir"
        os.makedirs(os.path.join(self.test_dir, "postmortems"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "logs"), exist_ok=True)
        self.fsm_path = os.path.join(self.test_dir, "fdc_fsm.json")
        self.postmortem_template = os.path.join(self.test_dir, "postmortem.md")
        self.plan_file = os.path.join(self.test_dir, "plan.txt")

        with open(self.fsm_path, "w") as f:
            json.dump({"start_state": "START", "accept_states": ["END"]}, f)
        with open(self.postmortem_template, "w") as f:
            f.write("Post-mortem template")
        with open(self.plan_file, "w") as f:
            f.write("set_plan\nTest plan")

        # Patch the paths to use our temporary files
        patcher_root = patch("tooling.fdc_cli.ROOT_DIR", self.test_dir)
        patcher_root.start()
        self.addCleanup(patcher_root.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("tooling.fdc_cli.start_task")
    def test_start_command(self, mock_start):
        """Tests the 'start' command."""
        with patch(
            "sys.argv", ["tooling/fdc_cli.py", "start", "--task-id", "task-123"]
        ):
            fdc_main()
        mock_start.assert_called_once_with("task-123")

    @patch("tooling.fdc_cli.close_task")
    def test_close_command(self, mock_close):
        """Tests the 'close' command."""
        with patch(
            "sys.argv", ["tooling/fdc_cli.py", "close", "--task-id", "task-123"]
        ):
            fdc_main()
        mock_close.assert_called_once_with("task-123")

    @patch("tooling.fdc_cli.validate_plan")
    def test_validate_command(self, mock_validate):
        """Tests the 'validate' command."""
        with patch("sys.argv", ["tooling/fdc_cli.py", "validate", self.plan_file]):
            fdc_main()
        mock_validate.assert_called_once_with(self.plan_file)

    @patch("tooling.fdc_cli.analyze_plan")
    def test_analyze_command(self, mock_analyze):
        """Tests the 'analyze' command."""
        with patch("sys.argv", ["tooling/fdc_cli.py", "analyze", self.plan_file]):
            fdc_main()
        mock_analyze.assert_called_once_with(self.plan_file)

    def test_missing_args(self):
        """Tests that the CLI exits when required args are missing."""
        with patch("sys.argv", ["tooling/fdc_cli.py", "start"]):  # Missing --task-id
            with self.assertRaises(SystemExit):
                fdc_main()


if __name__ == "__main__":
    unittest.main()
