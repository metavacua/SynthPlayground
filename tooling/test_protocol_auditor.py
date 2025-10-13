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

    @patch('tooling.protocol_auditor.run_protocol_source_check')
    def test_end_to_end_report_generation(self, mock_source_check):
        """
        Run the main function end-to-end and verify the content
        of the generated Markdown report.
        """
        mock_source_check.return_value = {
            "status": "success",
            "message": "AGENTS.md appears to be up-to-date."
        }

        # Store mock files and their content
        mock_files = {
            os.path.abspath("logs/activity.log.jsonl"): self.mock_log_content,
            os.path.abspath("AGENTS.md"): self.mock_agents_md_content,
        }

        # This will hold the content written to the report
        report_content_holder = {}

        # The actual path where the report will be written
        report_path = os.path.abspath(self.mock_report_path)

        # Custom side effect for mock_open
        def open_side_effect(filepath, mode='r', *args, **kwargs):
            abs_path = os.path.abspath(filepath)
            if mode == 'r':
                if abs_path in mock_files:
                    return mock_open(read_data=mock_files[abs_path]).return_value
                else:
                    # Return an empty file for any other read operations
                    return mock_open(read_data="").return_value
            elif mode == 'w' and abs_path == report_path:
                # Capture the written content for the report
                def write_side_effect(content):
                    report_content_holder['content'] = content

                mock_file_handle = mock_open().return_value
                mock_file_handle.write.side_effect = write_side_effect
                return mock_file_handle
            else:
                # Fallback for any other write operations
                return mock_open().return_value

        with patch('builtins.open', side_effect=open_side_effect) as mock_file_open:
            # Run the main auditor function
            protocol_auditor.main()

        # Check that the report file was opened for writing
        mock_file_open.assert_any_call(report_path, "w")

        # Get the content that was written to the report file
        written_content = report_content_holder.get('content', '')
        self.assertTrue(written_content, "Report file was not written to.")

        # --- Assertions on Report Content ---
        self.assertIn("`tool_D`", written_content)
        self.assertIn("`tooling/some_script.py`", written_content)
        self.assertIn("`tool_B`", written_content)
        self.assertIn("`tool_C`", written_content)
        self.assertIn("| `run_in_bash_session` | 1 |", written_content)
        self.assertIn("| `tool_A` | 1 |", written_content)
        self.assertIn("| `tooling/some_script.py` | 1 |", written_content)
        self.assertIn("| `tool_D` | 1 |", written_content)

if __name__ == '__main__':
    unittest.main()