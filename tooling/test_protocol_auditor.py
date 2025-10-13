import unittest
import os
import json
import sys
from unittest.mock import patch, mock_open

# Ensure the tooling directory is in the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import protocol_auditor

class TestProtocolAuditor(unittest.TestCase):
    """Test suite for the protocol_auditor.py script."""

    def setUp(self):
        """Set up mock files for testing."""
        self.mock_agents_md_content = """
# AGENTS.md Title

This is some introductory text.

```json
{
  "protocol_id": "protocol-1",
  "description": "First protocol.",
  "associated_tools": ["tool_A", "tool_B", "run_in_bash_session"]
}
```

Some markdown separating the blocks.

```json
{
  "protocol_id": "protocol-2",
  "description": "Second protocol with rules.",
  "rules": [
    {
      "rule_id": "rule-2.1",
      "description": "A specific rule.",
      "associated_tools": ["tool_C"]
    }
  ]
}
```
"""
        self.mock_log_content = """
{"action": {"type": "TOOL_EXEC", "details": {"tool_name": "tool_A", "parameters": {"some-arg": "value"}}}}
{"action": {"type": "OTHER_ACTION", "details": {}}}{"action": {"type": "TOOL_EXEC", "details": {"tool_name": "tooling/some_script.py"}}}
{"action": {"type": "TOOL_EXEC", "details": {"tool_name": "tool_D", "parameters": {"unlisted": true}}}}
{"action": {"type": "TOOL_EXEC", "details": {"tool_name": "run_in_bash_session", "parameters": {"command": "ls -l"}}}}
This is not a JSON line and should be skipped.
"""
        self.mock_report_path = "audit_report.md"

    def tearDown(self):
        """Clean up any created files."""
        if os.path.exists(self.mock_report_path):
            os.remove(self.mock_report_path)

    def test_get_protocol_tools_from_agents_md(self):
        """
        Verify that `get_protocol_tools_from_agents_md` correctly parses all
        JSON blocks from a mock AGENTS.md file.
        """
        mock_file = mock_open(read_data=self.mock_agents_md_content)
        with patch("builtins.open", mock_file):
            protocol_tools = protocol_auditor.get_protocol_tools_from_agents_md("dummy_path")
            expected_tools = {"tool_A", "tool_B", "run_in_bash_session", "tool_C"}
            self.assertEqual(protocol_tools, expected_tools)

    def test_get_used_tools_from_log(self):
        """
        Verify that `get_used_tools_from_log` correctly extracts tool names
        from a mock activity log file using the modern `tool_name` schema.
        """
        mock_file = mock_open(read_data=self.mock_log_content)
        with patch("builtins.open", mock_file):
            used_tools = protocol_auditor.get_used_tools_from_log("dummy_path")
            expected_tools = ["tool_A", "tooling/some_script.py", "tool_D", "run_in_bash_session"]
            self.assertCountEqual(used_tools, expected_tools)

    @patch('protocol_auditor.get_protocol_tools_from_agents_md')
    @patch('protocol_auditor.get_used_tools_from_log')
    @patch('protocol_auditor.run_protocol_source_check')
    @patch('protocol_auditor.find_all_agents_md_files')
    def test_end_to_end_report_generation(self, mock_find_files, mock_source_check, mock_get_used_tools, mock_get_protocol_tools):
    @patch('protocol_auditor.run_protocol_source_check')
    def test_end_to_end_report_generation(self, mock_source_check):
        """
        Run the main function end-to-end by mocking the data gathering functions
        and verifying the content of the generated Markdown report.
        """
        # Mock the data gathering functions to return controlled data
        mock_find_files.return_value = ['/mock/path/to/AGENTS.md']
        mock_get_used_tools.return_value = ["tool_A", "tooling/some_script.py", "tool_D", "run_in_bash_session"]
        mock_get_protocol_tools.return_value = {"tool_A", "tool_B", "run_in_bash_session", "tool_C"}
        mock_source_check.return_value = [{"status": "success", "message": "AGENTS.md appears to be up-to-date."}]

        # Use a real file handle for the report writing to inspect the output
        with patch("builtins.open", mock_open()) as mock_opener:
            # Run the main auditor function
            protocol_auditor.main()

            # The auditor calculates an absolute path, so we must check for that.
            expected_report_path = os.path.abspath(self.mock_report_path)

            # Check that the report was written to the correct file
            mock_opener.assert_any_call(expected_report_path, "w")

            # Get the content that was written to the report file
            mock_write_handle = mock_opener()
            written_content = mock_write_handle.write.call_args[0][0]

            # --- Assertions on Report Content ---
            self.assertIn("`tool_D`", written_content)
            self.assertIn("`tooling/some_script.py`", written_content)
            self.assertIn("`tool_B`", written_content)
            self.assertIn("`tool_C`", written_content)
            self.assertIn("| `run_in_bash_session` | 1 |", written_content)
            self.assertIn("| `tool_A` | 1 |", written_content)
            self.assertIn("| `tooling/some_script.py` | 1 |", written_content)
            self.assertIn("| `tool_D` | 1 |", written_content)
        # Mock the source check to return a success state
        mock_source_check.return_value = [{
            "status": "success",
            "message": "AGENTS.md appears to be up-to-date."
        }]

        # Create a mock handle specifically for the write operation
        mock_write_handle = mock_open().return_value

        # This dictionary will map filepaths to their mock content
        mock_files = {
            os.path.abspath(protocol_auditor.LOG_FILE): self.mock_log_content,
            # We will only mock one AGENTS.md for this test to keep it simple
            os.path.abspath("AGENTS.md"): self.mock_agents_md_content,
            os.path.abspath(self.mock_report_path): "" # For the write
        }

        # The new side effect function for `open`
        def open_side_effect(path, mode='r'):
            path = os.path.abspath(path)
            if mode == 'w':
                # This handles the report writing
                return mock_write_handle

            # This handles reading from our mocked files
            content = mock_files.get(path, "") # Default to empty for other files
            return mock_open(read_data=content).return_value

        # We also need to mock find_all_agents_md_files to control its output
        with patch("builtins.open", open_side_effect), \
             patch("protocol_auditor.find_all_agents_md_files", return_value=[os.path.abspath("AGENTS.md")]):
            protocol_auditor.main()

        # The auditor calculates an absolute path, so we must check for that.
        expected_report_path = os.path.abspath(self.mock_report_path)

        # Check that the report was written to the correct file
        mock_write_handle.write.assert_called_once()

        # Get the content that was written to the report file
        written_content = mock_write_handle.write.call_args[0][0]

        # --- Assertions on Report Content ---
        # Check for unreferenced tools (used but not in protocol)
        self.assertIn("`tool_D`", written_content)
        self.assertIn("`tooling/some_script.py`", written_content)

        # Check for unused protocol tools (in protocol but not used)
        self.assertIn("`tool_B`", written_content)
        self.assertIn("`tool_C`", written_content)

        # Check for tool centrality counts
        self.assertIn("| `run_in_bash_session` | 1 |", written_content)
        self.assertIn("| `tool_A` | 1 |", written_content)
        self.assertIn("| `tooling/some_script.py` | 1 |", written_content)
        self.assertIn("| `tool_D` | 1 |", written_content)

    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_all_agents_md_files_with_special_dirs(self, mock_walk, mock_getmtime):
        """
        Verify that `find_all_agents_md_files` correctly ignores directories
        listed in the SPECIAL_DIRS configuration.
        """
        # --- Mock Filesystem Setup ---
        # This setup simulates a root AGENTS.md, a nested one, and one in a special dir.
        mock_fs = {
            os.path.abspath('.'): (['core', 'protocols', 'protocols/security'], ['AGENTS.md', 'README.md']),
            os.path.abspath('./core'): (['protocols'], ['AGENTS.md']),
            os.path.abspath('./core/protocols'): ([], ['some.protocol.md']),
            os.path.abspath('./protocols'): ([], ['main.protocol.md']),
            os.path.abspath('./protocols/security'): ([], ['AGENTS.md']), # This should be ignored
        }

        # The first element of the tuple is directories, the second is files.
        def walk_side_effect(path, topdown=True):
            if path in mock_fs:
                dirs, files = mock_fs[path]
                yield path, dirs, files
                for d in dirs:
                    # This recursive call is the key to making the mock work
                    yield from walk_side_effect(os.path.join(path, d))
            else:
                yield path, [], [] # Stop walking if path not in mock_fs

        mock_walk.side_effect = walk_side_effect

        # --- Execution ---
        # The auditor's ROOT_DIR is the parent of the tooling dir, so we call it from there.
        auditor_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        found_files = protocol_auditor.find_all_agents_md_files(auditor_root)

        # --- Assertions ---
        # Convert to relative paths for easier comparison
        relative_found_files = {os.path.relpath(p, auditor_root) for p in found_files}

        self.assertIn('AGENTS.md', relative_found_files)
        self.assertIn('core/AGENTS.md', relative_found_files)
        self.assertNotIn('protocols/security/AGENTS.md', relative_found_files)
        self.assertEqual(len(relative_found_files), 2)


if __name__ == '__main__':
    unittest.main()