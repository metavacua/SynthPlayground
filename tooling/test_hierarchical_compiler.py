import unittest
import os
import shutil
import json
from unittest.mock import patch, MagicMock, call
from tooling.hierarchical_compiler import (
    find_protocol_dirs,
    generate_summary,
    main as hierarchical_main,
)


class TestHierarchicalCompiler(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_hierarchical_compiler_dir"
        self.root_protocols = os.path.join(self.test_dir, "protocols")
        self.child_protocols = os.path.join(self.test_dir, "child", "protocols")
        os.makedirs(self.root_protocols, exist_ok=True)
        os.makedirs(self.child_protocols, exist_ok=True)

        # Mock the external compiler and generator scripts
        patcher_compiler = patch("tooling.hierarchical_compiler.run_compiler")
        self.mock_run_compiler = patcher_compiler.start()
        self.addCleanup(patcher_compiler.stop)

        patcher_readme = patch("tooling.hierarchical_compiler.run_readme_generator")
        self.mock_run_readme = patcher_readme.start()
        self.addCleanup(patcher_readme.stop)

        patcher_kg = patch(
            "tooling.hierarchical_compiler.compile_centralized_knowledge_graph"
        )
        self.mock_compile_kg = patcher_kg.start()
        self.addCleanup(patcher_kg.stop)

        # Set the ROOT_DIR to our test directory
        patcher_root = patch("tooling.hierarchical_compiler.ROOT_DIR", self.test_dir)
        patcher_root.start()
        self.addCleanup(patcher_root.stop)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_protocol_dirs_bottom_up(self):
        """Tests that protocol directories are found in deepest-first order."""
        # The setup already creates the directories
        dirs = find_protocol_dirs(self.test_dir)
        self.assertEqual(len(dirs), 2)
        # The child directory should come first because it's deeper
        self.assertEqual(dirs[0], self.child_protocols)
        self.assertEqual(dirs[1], self.root_protocols)

    def test_generate_summary(self):
        """Tests the generation of a summary from a child AGENTS.md."""
        child_agents_md = os.path.join(self.test_dir, "child", "AGENTS.md")
        with open(child_agents_md, "w") as f:
            f.write(
                """
# Protocol: Child Protocol
This is the child's protocol.
```json
{"protocol_id": "CHILD-001"}
```
---
"""
            )
        summary = generate_summary(child_agents_md)
        self.assertIn("# --- Child Module: `child` ---", summary)
        self.assertIn("# Protocol: Child Protocol", summary)
        self.assertIn("CHILD-001", summary)

    def test_main_orchestration(self):
        """Tests the main orchestration logic of the hierarchical compiler."""
        # Define what the mocked compilers should return
        child_agents_path = os.path.join(self.test_dir, "child", "AGENTS.md")
        root_agents_path = os.path.join(self.test_dir, "AGENTS.md")

        # Simulate the compiler creating the AGENTS.md files
        self.mock_run_compiler.side_effect = [child_agents_path, root_agents_path]

        # Create dummy AGENTS.md for summary generation to work
        with open(child_agents_path, "w") as f:
            f.write("# Protocol: Child Protocol\n---\n")

        hierarchical_main()

        # Check that the compilers were called in the correct order (child then root)
        calls = self.mock_run_compiler.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], call(self.child_protocols))
        self.assertEqual(calls[1], call(self.root_protocols))

        # Check that README generation was called for each compiled AGENTS.md
        self.assertEqual(self.mock_run_readme.call_count, 2)

        # Check that the summary was created in the parent's protocol dir
        summary_file_path = os.path.join(
            self.root_protocols, "_z_child_summary_child.protocol.md"
        )
        self.assertTrue(os.path.exists(summary_file_path))

        # Check that the centralized KG compilation was called at the end
        self.mock_compile_kg.assert_called_once()


if __name__ == "__main__":
    unittest.main()
