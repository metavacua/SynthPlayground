import unittest
import os
import json
import shutil
from unittest.mock import patch
from tooling.self_correction_orchestrator import (
    load_lessons,
    save_lessons,
    process_lessons,
    main,
)


class TestSelfCorrectionOrchestrator(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_self_correction_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.lessons_file = os.path.join(self.test_dir, "lessons.jsonl")

        # Mocking the external scripts and file paths
        patcher_run = patch(
            "tooling.self_correction_orchestrator.run_command", return_value=True
        )
        self.mock_run_command = patcher_run.start()
        self.addCleanup(patcher_run.stop)

        patcher_lessons_file = patch(
            "tooling.self_correction_orchestrator.LESSONS_FILE", self.lessons_file
        )
        patcher_lessons_file.start()
        self.addCleanup(patcher_lessons_file.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_and_save_lessons(self):
        """Tests that lessons can be loaded from and saved to the JSONL file."""
        lessons_data = [
            {"lesson_id": "L001", "status": "pending"},
            {"lesson_id": "L002", "status": "applied"},
        ]
        with open(self.lessons_file, "w") as f:
            for lesson in lessons_data:
                f.write(json.dumps(lesson) + "\n")

        loaded = load_lessons()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["lesson_id"], "L001")

        loaded[0]["status"] = "failed"
        save_lessons(loaded)

        reloaded = load_lessons()
        self.assertEqual(reloaded[0]["status"], "failed")

    @patch("tooling.self_correction_orchestrator.UPDATER_SCRIPT", "mock_updater.py")
    def test_process_update_protocol_lesson(self):
        """Tests processing a lesson that updates a protocol."""
        lessons = [
            {
                "lesson_id": "L001",
                "status": "pending",
                "action": {
                    "type": "UPDATE_PROTOCOL",
                    "command": "add-tool",
                    "parameters": {"protocol_id": "p-123", "tool_name": "new-tool"},
                },
            }
        ]

        changes_made = process_lessons(lessons, "protocols_dir")
        self.assertTrue(changes_made)
        self.assertEqual(lessons[0]["status"], "applied")
        self.mock_run_command.assert_called_once_with(
            [
                "python3",
                "mock_updater.py",
                "--protocols-dir",
                "protocols_dir",
                "add-tool",
                "--protocol-id",
                "p-123",
                "--tool-name",
                "new-tool",
            ]
        )

    @patch(
        "tooling.self_correction_orchestrator.CODE_SUGGESTER_SCRIPT",
        "mock_suggester.py",
    )
    def test_process_code_change_lesson(self):
        """Tests processing a lesson that proposes a code change."""
        lessons = [
            {
                "lesson_id": "L002",
                "status": "pending",
                "action": {
                    "type": "PROPOSE_CODE_CHANGE",
                    "parameters": {
                        "filepath": "src/main.py",
                        "diff": "@@ -1,1 +1,1 @@\n-old\n+new",
                    },
                },
            }
        ]

        changes_made = process_lessons(lessons, ".")
        self.assertTrue(changes_made)
        self.assertEqual(lessons[0]["status"], "applied")
        self.mock_run_command.assert_called_once_with(
            [
                "python3",
                "mock_suggester.py",
                "--filepath",
                "src/main.py",
                "--diff",
                "@@ -1,1 +1,1 @@\n-old\n+new",
            ]
        )

    def test_failed_command(self):
        """Tests that lesson status is set to 'failed' when a command fails."""
        self.mock_run_command.return_value = False
        lessons = [
            {
                "lesson_id": "L003",
                "status": "pending",
                "action": {
                    "type": "UPDATE_PROTOCOL",
                    "command": "add-tool",
                    "parameters": {"protocol_id": "p-456", "tool_name": "another-tool"},
                },
            }
        ]

        changes_made = process_lessons(lessons, ".")
        self.assertTrue(changes_made)
        self.assertEqual(lessons[0]["status"], "failed")

    @patch("tooling.self_correction_orchestrator.process_lessons", return_value=True)
    def test_main_flow_rebuilds_agents_md(self, mock_process):
        """Tests that the main function calls to rebuild AGENTS.md after changes."""
        with open(self.lessons_file, "w") as f:
            f.write(json.dumps({"lesson_id": "L001", "status": "pending"}) + "\n")

        main()

        # Check that process_lessons was called
        mock_process.assert_called()

        # Check that 'make AGENTS.md' was called
        self.mock_run_command.assert_called_with(["make", "AGENTS.md"])

    def test_no_pending_lessons(self):
        """Tests that the orchestrator does nothing if there are no pending lessons."""
        lessons = [{"lesson_id": "L001", "status": "applied"}]
        with open(self.lessons_file, "w") as f:
            for lesson in lessons:
                f.write(json.dumps(lesson) + "\n")

        main()

        # process_lessons should not be called if there are no pending lessons.
        # Note: This tests the main() function's initial check.
        self.mock_run_command.assert_not_called()

    def test_malformed_lesson(self):
        """Tests that malformed lessons are skipped and status is not changed."""
        lessons = [{"lesson_id": "L001", "status": "pending"}]  # Missing "action"
        changes_made = process_lessons(lessons, ".")
        self.assertFalse(changes_made)
        self.assertEqual(
            lessons[0]["status"], "pending"
        )  # Status should remain pending

    def test_unknown_action_type(self):
        """Tests that lessons with unknown action types are skipped."""
        lessons = [
            {
                "lesson_id": "L001",
                "status": "pending",
                "action": {"type": "UNKNOWN_ACTION"},
            }
        ]
        changes_made = process_lessons(lessons, ".")
        self.assertFalse(changes_made)
        self.assertEqual(lessons[0]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
