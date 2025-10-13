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

    @patch('tooling.protocol_auditor.find_all_agents_md_files')
    @patch('tooling.protocol_auditor.run_protocol_source_check')
    def test_end_to_end_report_generation(self, mock_run_source_check, mock_find_agents):
        """
        Run the main function end-to-end and verify the content
        of the generated Markdown report.
        """
        mock_find_agents.return_value = ['/app/AGENTS.md']
        mock_run_source_check.return_value = [{"status": "success", "message": "All AGENTS.md files appear to be up-to-date."}]

        mock_files = {
            protocol_auditor.LOG_FILE: mock_open(read_data=self.mock_log_content).return_value,
            '/app/AGENTS.md': mock_open(read_data=self.mock_agents_md_content).return_value,
            os.path.join(protocol_auditor.ROOT_DIR, "audit_report.md"): mock_open().return_value
        }

        def mock_open_side_effect(path, *args, **kwargs):
            # Normalize the path to handle potential relative vs. absolute mismatches
            normalized_path = os.path.abspath(path)
            if normalized_path in mock_files:
                return mock_files[normalized_path]
            # Fallback for any other open calls that are not mocked
            return mock_open().return_value

        with patch('builtins.open', side_effect=mock_open_side_effect):
            # Run the main auditor function
            protocol_auditor.main()

        # Get the mock for the report file to check what was written
        report_mock_handle = mock_files[os.path.abspath(self.mock_report_path)]

        # Get the content that was written to the report file
        written_content = report_mock_handle.write.call_args[0][0]

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

    def test_run_enforcement_check(self):
        """
        Tests the `run_enforcement_check` function to ensure it flags protocols
        with prohibitory language but no `enforcement` key.
        """
        mock_content_with_violation = """
```json
{
  "protocol_id": "test-prohibit-001",
  "rules": [
    {
      "rule_id": "no-silly-business",
      "description": "This rule is here to forbid silly business."
    }
  ]
}
```
```json
{
  "protocol_id": "test-prohibit-002",
  "rules": [
    {
      "rule_id": "must-be-serious",
      "description": "This rule is to prohibit fun.",
      "enforcement": "This is enforced by the fun police."
    }
  ]
}
```
"""
        mock_file = mock_open(read_data=mock_content_with_violation)
        with patch("builtins.open", mock_file):
            violations = protocol_auditor.run_enforcement_check(["dummy_path"])
            self.assertEqual(len(violations), 1)
            self.assertEqual(violations[0]["protocol_id"], "test-prohibit-001")
            self.assertIn("unenforced prohibition", violations[0]["message"])


if __name__ == '__main__':
    unittest.main()