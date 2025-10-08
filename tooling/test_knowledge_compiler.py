import unittest
import os
from tooling.knowledge_compiler import (
    extract_lessons_from_postmortem,
    extract_metadata_from_postmortem,
    main as compile_main,
)


class TestKnowledgeCompiler(unittest.TestCase):

    def setUp(self):
        self.mock_postmortem_content = """
# Post-Mortem Report

**Task ID:** `test/sample-task-01`
**Completion Date:** `2025-10-07`

---

## 1. Task Summary
A summary of the task.

---

## 2. Process Analysis
Analysis here.

---

## 3. Corrective Actions & Lessons Learned

1. **Lesson:** This is the first lesson.
   **Action:** This is the first action.
2. **Lesson:** This is the second,
multi-line lesson.
   **Action:** This is the second,
multi-line action.

---
"""
        self.test_postmortem_path = "test_postmortem.md"
        with open(self.test_postmortem_path, "w") as f:
            f.write(self.mock_postmortem_content)

        self.lessons_learned_path = "knowledge_core/lessons_learned.md"
        # Backup original lessons if it exists
        if os.path.exists(self.lessons_learned_path):
            os.rename(self.lessons_learned_path, self.lessons_learned_path + ".bak")
        # Create a blank one for the test
        with open(self.lessons_learned_path, "w") as f:
            f.write("# Lessons Learned\n\n")

    def tearDown(self):
        if os.path.exists(self.test_postmortem_path):
            os.remove(self.test_postmortem_path)

        # Clean up the test lessons learned and restore backup
        if os.path.exists(self.lessons_learned_path):
            os.remove(self.lessons_learned_path)
        if os.path.exists(self.lessons_learned_path + ".bak"):
            os.rename(self.lessons_learned_path + ".bak", self.lessons_learned_path)

    def test_extract_metadata(self):
        metadata = extract_metadata_from_postmortem(self.mock_postmortem_content)
        self.assertEqual(metadata["task_id"], "test/sample-task-01")
        self.assertEqual(metadata["date"], "2025-10-07")

    def test_extract_lessons(self):
        lessons = extract_lessons_from_postmortem(self.mock_postmortem_content)
        self.assertEqual(len(lessons), 2)
        self.assertEqual(lessons[0]["lesson"], "This is the first lesson.")
        self.assertEqual(lessons[0]["action"], "This is the first action.")
        self.assertEqual(lessons[1]["lesson"], "This is the second, multi-line lesson.")
        self.assertEqual(lessons[1]["action"], "This is the second, multi-line action.")

    def test_main_compiler_function(self):
        # The main function takes command line args, so we'll simulate that
        import sys

        original_argv = sys.argv
        sys.argv = ["knowledge_compiler.py", self.test_postmortem_path]

        compile_main()

        sys.argv = original_argv  # Restore original argv

        with open(self.lessons_learned_path, "r") as f:
            content = f.read()

        self.assertIn("Insight:** This is the first lesson.", content)
        self.assertIn("Actionable Guidance:** This is the first action.", content)
        self.assertIn("Insight:** This is the second, multi-line lesson.", content)
        self.assertIn(
            "Actionable Guidance:** This is the second, multi-line action.", content
        )
        self.assertIn("Task ID:** test/sample-task-01", content)


if __name__ == "__main__":
    unittest.main()
