"""
Unit tests for the self_correction_orchestrator.py script.

This test suite verifies the end-to-end functionality of the automated
self-correction workflow. It ensures that the orchestrator can correctly
read structured lessons, invoke the protocol_updater.py script as a
subprocess with the correct arguments, and update the lesson status file
to reflect the outcome.
"""

import unittest
import os
import json
import tempfile
import shutil
from tooling.self_correction_orchestrator import (
    process_lessons,
    load_lessons,
    save_lessons,
)


class TestSelfCorrectionOrchestrator(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with mock files."""
        self.test_dir = tempfile.mkdtemp()

        # Mock the lessons file
        self.lessons_file_path = os.path.join(self.test_dir, "lessons.jsonl")
        self.initial_lessons = [
            {
                "lesson_id": "l1",
                "insight": "Tool 'new_tool' should be in protocol 'p1'.",
                "action": {
                    "type": "UPDATE_PROTOCOL",
                    "command": "add-tool",
                    "parameters": {"protocol_id": "p1", "tool_name": "new_tool"},
                },
                "status": "pending",
            },
            {
                "lesson_id": "l2",
                "insight": "This one is already done.",
                "action": {},
                "status": "applied",
            },
        ]
        with open(self.lessons_file_path, "w") as f:
            for lesson in self.initial_lessons:
                f.write(json.dumps(lesson) + "\n")

        # Mock the protocols directory and a protocol file
        self.protocols_dir_path = os.path.join(self.test_dir, "protocols")
        os.makedirs(self.protocols_dir_path)
        self.protocol_file_path = os.path.join(
            self.protocols_dir_path, "p1.protocol.json"
        )
        self.initial_protocol_data = {
            "protocol_id": "p1",
            "associated_tools": ["existing_tool"],
        }
        with open(self.protocol_file_path, "w") as f:
            json.dump(self.initial_protocol_data, f, indent=2)

        # --- Monkey-patch the constants in the orchestrator to use our temp files ---
        import tooling.self_correction_orchestrator as orchestrator

        self.orchestrator_orig_lessons = orchestrator.LESSONS_FILE
        orchestrator.LESSONS_FILE = self.lessons_file_path

    def tearDown(self):
        """Clean up and restore original constants."""
        shutil.rmtree(self.test_dir)
        import tooling.self_correction_orchestrator as orchestrator

        orchestrator.LESSONS_FILE = self.orchestrator_orig_lessons

    def test_process_lessons_end_to_end(self):
        """
        Verify the entire workflow: loading, processing, saving,
        and checking the side-effects (protocol file updated).
        """
        # Load initial lessons
        lessons = load_lessons()
        self.assertEqual(len(lessons), 2)

        # Run the processing, passing the mock protocols directory
        changes_made = process_lessons(lessons, self.protocols_dir_path)
        self.assertTrue(changes_made)

        # Save the updated lessons
        save_lessons(lessons)

        # --- Verification ---
        # 1. Verify the protocol file was updated
        with open(self.protocol_file_path, "r") as f:
            updated_protocol = json.load(f)
        self.assertIn("new_tool", updated_protocol["associated_tools"])
        self.assertEqual(len(updated_protocol["associated_tools"]), 2)

        # 2. Verify the lessons file was updated
        updated_lessons = load_lessons()
        self.assertEqual(updated_lessons[0]["status"], "applied")
        self.assertEqual(updated_lessons[1]["status"], "applied")  # Stays the same

    def test_process_lessons_handles_malformed_lesson_gracefully(self):
        """
        Verify that the orchestrator can skip a malformed lesson without crashing.
        A malformed lesson, in this context, is one that is pending but is
        missing the required 'command' key in its action payload.
        """
        # --- Setup: Add a malformed lesson to the existing ones ---
        malformed_lesson = {
            "lesson_id": "l3-malformed",
            "insight": "This lesson is broken.",
            "action": {
                "type": "UPDATE_PROTOCOL",
                # "command" key is intentionally missing
                "parameters": {"protocol_id": "p-broken", "tool_name": "t-broken"},
            },
            "status": "pending",
        }
        # The valid lesson from the initial setup
        valid_lesson = self.initial_lessons[0]

        # Overwrite the lessons file with a new list
        lessons_with_malformed = [valid_lesson, malformed_lesson]
        save_lessons(lessons_with_malformed)

        # --- Execution ---
        # Run the processing. This should not raise an exception.
        changes_made = process_lessons(lessons_with_malformed, self.protocols_dir_path)
        self.assertTrue(
            changes_made, "Should report changes since the valid lesson was processed."
        )

        # Save the results back to the file before verifying
        save_lessons(lessons_with_malformed)

        # --- Verification ---
        # 1. Verify the protocol file for the *valid* lesson was updated
        with open(self.protocol_file_path, "r") as f:
            updated_protocol = json.load(f)
        self.assertIn("new_tool", updated_protocol["associated_tools"])

        # 2. Verify the statuses of the lessons
        final_lessons = load_lessons()
        # The valid lesson should be 'applied'
        self.assertEqual(final_lessons[0]["status"], "applied")
        # The malformed lesson should still be 'pending' as it was skipped
        self.assertEqual(final_lessons[1]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
