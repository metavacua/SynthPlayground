import unittest
import os
import shutil
from unittest.mock import patch
from tooling.background_researcher import perform_research


class TestBackgroundResearcher(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_background_researcher_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.task_id = "test_task_123"
        self.result_path = f"/tmp/{self.task_id}.result"

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if os.path.exists(self.result_path):
            os.remove(self.result_path)

    @patch("time.sleep", return_value=None)
    def test_perform_research(self, mock_sleep):
        """Tests that the research script writes the correct result file."""
        perform_research(self.task_id)

        self.assertTrue(os.path.exists(self.result_path))
        with open(self.result_path, "r") as f:
            content = f.read()

        self.assertEqual(
            content, f"This is the research result for task {self.task_id}."
        )
        mock_sleep.assert_called_once_with(5)


if __name__ == "__main__":
    unittest.main()
