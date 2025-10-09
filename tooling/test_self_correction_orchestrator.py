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
from tooling.self_correction_orchestrator import process_lessons, load_lessons, save_lessons

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
                    "parameters": {"protocol_id": "p1", "tool_name": "new_tool"}
                },
                "status": "pending"
            },
            {
                "lesson_id": "l2",
                "insight": "This one is already done.",
                "action": {},
                "status": "applied"
            }
        ]
        with open(self.lessons_file_path, "w") as f:
            for lesson in self.initial_lessons:
                f.write(json.dumps(lesson) + "\n")

        # Mock the protocols directory and a protocol file
        self.protocols_dir_path = os.path.join(self.test_dir, "protocols")
        os.makedirs(self.protocols_dir_path)
        self.protocol_file_path = os.path.join(self.protocols_dir_path, "p1.protocol.json")
        self.initial_protocol_data = {
            "protocol_id": "p1",
            "associated_tools": ["existing_tool"]
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
        self.assertEqual(updated_lessons[1]["status"], "applied") # Stays the same

if __name__ == "__main__":
    unittest.main()