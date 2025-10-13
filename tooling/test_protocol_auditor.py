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

    @patch('protocol_auditor.find_all_agents_md_files')
    @patch('os.path.getmtime')
    def test_end_to_end_report_generation(self, mock_getmtime, mock_find_agents):
        """
        Run the main function end-to-end and verify the content
        of the generated Markdown report.
        """
        # Mock the filesystem interaction
        mock_find_agents.return_value = ['/app/protocols/AGENTS.md']
        # Mock mtime to prevent source check warnings. Make source older than agent file.
        mock_getmtime.side_effect = [100, 50] # AGENTS.md is newer

        # Create a mock handle specifically for the write operation
        mock_write_handle = mock_open().return_value

        # Patch the file reads and the final write
        m = mock_open()
        with patch("builtins.open", m) as mock_file:
            # Configure mock to handle different files
            # The order is now: 1. log file, 2. the single AGENTS.md, 3. the output report
            mock_file.side_effect = [
                mock_open(read_data=self.mock_log_content).return_value,
                mock_open(read_data=self.mock_agents_md_content).return_value,
                mock_write_handle,
            ]

            # Run the main auditor function
            with patch('os.path.isdir', return_value=True): # Assume protocols dir exists
                 protocol_auditor.main()

        # The auditor calculates an absolute path, so we must check for that.
        expected_report_path = os.path.abspath(self.mock_report_path)

        # Check that the report was written to the correct file
        m.assert_any_call(expected_report_path, "w")

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

if __name__ == '__main__':
    unittest.main()