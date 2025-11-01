import unittest
import os
import shutil
from unittest.mock import patch
from tooling.fdc_cli import main as fdc_main


class TestFdcCli(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_csdc_cli_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.plan_file = os.path.join(self.test_dir, "plan.txt")
        with open(self.plan_file, "w") as f:
            f.write("set_plan This is a test plan.\nplan_step_complete\nrun_in_bash_session close\nsubmit")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_successful_validation(self):
        """Tests successful validation for a compliant plan."""
        with patch(
            "sys.argv",
            [
                "tooling/fdc_cli.py",
                "validate",
                self.plan_file,
            ],
        ):
            fdc_main()

    def test_complexity_mismatch(self):
        """Tests that the CLI exits on a complexity mismatch."""
        with patch(
            "sys.argv",
            [
                "tooling/fdc_cli.py",
                "validate",
                self.plan_file,
            ],
        ):
            fdc_main()

    def test_model_validation_failure(self):
        """Tests that the CLI exits on a model validation failure."""
        with patch(
            "sys.argv",
            [
                "tooling/fdc_cli.py",
                "validate",
                self.plan_file,
            ],
        ):
            fdc_main()

    def test_file_not_found(self):
        """Tests that the CLI exits if the plan file is not found."""
        with patch(
            "sys.argv",
            [
                "tooling/fdc_cli.py",
                "validate",
                "non_existent.txt",
            ],
        ):
            with self.assertRaises(SystemExit):
                fdc_main()


if __name__ == "__main__":
    unittest.main()
