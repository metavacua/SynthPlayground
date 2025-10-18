"""
Unit tests for the knowledge_compiler.py script.

This test suite verifies that the knowledge compiler can correctly parse
a mock post-mortem report and generate a structured, machine-readable
lessons.jsonl file. It ensures that the generated lessons conform to the
expected JSON schema, including having unique IDs and a 'pending' status.
"""

import unittest
import os
import json
import tempfile
import shutil
from tooling.knowledge_compiler import main as compile_knowledge


class TestKnowledgeCompiler(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with mock files."""
        self.test_dir = tempfile.mkdtemp()

        # Mock post-mortem file
        self.postmortem_path = os.path.join(self.test_dir, "test_postmortem.md")
        postmortem_content = """
# Post-Mortem Report
**Task ID:** `test-task-123`
**Completion Date:** `2025-01-01`
---
## 3. Corrective Actions & Lessons Learned
1.  **Lesson:** A tool was used that was not in the protocol.
    **Action:** Add tool 'newly_used_tool' to protocol 'fdc-protocol-001'.
2.  **Lesson:** The agent needs to be more careful.
    **Action:** This is a free-text action that is not machine-readable.
---
"""
        with open(self.postmortem_path, "w") as f:
            f.write(postmortem_content)

        # Path for the output lessons file
        self.lessons_path = os.path.join(self.test_dir, "lessons.jsonl")

        # Monkey-patch the KNOWLEDGE_CORE_PATH to use our temp file
        import tooling.knowledge_compiler

        self.original_path = tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH
        tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH = self.lessons_path

        # Mock sys.argv
        import sys

        self.original_argv = sys.argv
        sys.argv = ["tooling/knowledge_compiler.py", self.postmortem_path]

    def tearDown(self):
        """Clean up the temporary directory and restore original state."""
        shutil.rmtree(self.test_dir)
        import tooling.knowledge_compiler

        tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH = self.original_path
        import sys

        sys.argv = self.original_argv

    def test_knowledge_compiler_end_to_end(self):
        """
        Verify that the compiler correctly parses a post-mortem and
        generates a structured lessons.jsonl file with both machine-readable
        and placeholder commands.
        """
        # Run the main function of the compiler
        compile_knowledge()

        # Verify the output file was created and has content
        self.assertTrue(os.path.exists(self.lessons_path))
        with open(self.lessons_path, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)

        # Verify the content of the generated lessons
        lesson1 = json.loads(lines[0])
        lesson2 = json.loads(lines[1])

        # Check lesson 1 (machine-readable)
        self.assertEqual(lesson1["task_id"], "test-task-123")
        self.assertEqual(
            lesson1["insight"], "A tool was used that was not in the protocol."
        )
        self.assertEqual(lesson1["status"], "pending")
        self.assertEqual(lesson1["action"]["command"], "add-tool")
        self.assertEqual(
            lesson1["action"]["parameters"]["tool_name"], "newly_used_tool"
        )
        self.assertEqual(
            lesson1["action"]["parameters"]["protocol_id"], "fdc-protocol-001"
        )

        # Check lesson 2 (placeholder)
        self.assertEqual(lesson2["insight"], "The agent needs to be more careful.")
        self.assertEqual(lesson2["status"], "pending")
        self.assertEqual(lesson2["action"]["command"], "placeholder")
        self.assertIn(
            "not machine-readable", lesson2["action"]["parameters"]["description"]
        )


class TestKnowledgeCompilerAdvanced(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for advanced parsing tests."""
        self.test_dir = tempfile.mkdtemp()
        self.postmortem_path = os.path.join(self.test_dir, "advanced_postmortem.md")
        # This mock post-mortem uses a different header and action format
        postmortem_content = """
# Post-Mortem: Advanced Failure Analysis
**Task ID:** `adv-test-456`
**Completion Date:** `2025-10-10`
---
## 5. Proposed Corrective Actions

1.  A tool is no longer suitable for a protocol.
    **Action:** Deprecate tool 'old_tool' from protocol 'legacy-protocol-002'.

2.  **Lesson:** The `reset_all` tool is dangerous and was used incorrectly.
    **Action:** The `self_improvement_cli.py` script should be updated to flag its usage.

3.  A new protocol `reset-all-authorization-001` will be created to programmatically block the execution of `reset_all()`.
---
"""
        with open(self.postmortem_path, "w") as f:
            f.write(postmortem_content)

        self.lessons_path = os.path.join(self.test_dir, "lessons.jsonl")
        import tooling.knowledge_compiler

        self.original_path = tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH
        tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH = self.lessons_path

        import sys

        self.original_argv = sys.argv
        sys.argv = ["tooling/knowledge_compiler.py", self.postmortem_path]

    def tearDown(self):
        """Clean up the temporary directory and restore original state."""
        shutil.rmtree(self.test_dir)
        import tooling.knowledge_compiler

        tooling.knowledge_compiler.KNOWLEDGE_CORE_PATH = self.original_path
        import sys

        sys.argv = self.original_argv

    def test_advanced_parsing_and_deprecate_command(self):
        """
        Verify the compiler can handle different section headers and parse
        the 'deprecate-tool' command.
        """
        compile_knowledge()

        self.assertTrue(os.path.exists(self.lessons_path))
        with open(self.lessons_path, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 3)

        lesson1 = json.loads(lines[0])
        lesson2 = json.loads(lines[1])
        lesson3 = json.loads(lines[2])

        # Test 1: Deprecate tool command
        self.assertIn("A tool is no longer suitable", lesson1["insight"])
        self.assertEqual(lesson1["action"]["command"], "deprecate-tool")
        self.assertEqual(lesson1["action"]["parameters"]["tool_name"], "old_tool")
        self.assertEqual(
            lesson1["action"]["parameters"]["protocol_id"], "legacy-protocol-002"
        )

        # Test 2: Explicit Lesson and Placeholder Action
        self.assertEqual(
            lesson2["insight"],
            "The `reset_all` tool is dangerous and was used incorrectly.",
        )
        self.assertEqual(lesson2["action"]["command"], "placeholder")
        self.assertIn(
            "should be updated to flag", lesson2["action"]["parameters"]["description"]
        )

        # Test 3: No explicit lesson, whole text becomes the action/insight
        self.assertIn("A new protocol", lesson3["insight"])
        self.assertEqual(lesson3["action"]["command"], "placeholder")


if __name__ == "__main__":
    unittest.main()
