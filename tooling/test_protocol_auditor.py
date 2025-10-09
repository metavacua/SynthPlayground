import unittest
import os
import json
import tempfile
import shutil
from tooling.protocol_auditor import (
    get_used_tools_from_log,
    get_protocol_tools_from_agents_md,
    run_completeness_check,
    run_centrality_analysis,
    run_protocol_source_check,
    generate_markdown_report
)

class TestProtocolAuditor(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with mock files for testing."""
        self.test_dir = tempfile.mkdtemp()

        # --- Create Mock AGENTS.md ---
        self.agents_md_path = os.path.join(self.test_dir, "AGENTS.md")
        agents_md_content = """
# Protocol V1
```json
{
  "protocol_id": "proto-1",
  "associated_tools": ["tool_A", "tool_B"]
}
```

Some text here.

# Protocol V2
```json
{
  "protocol_id": "proto-2",
  "rules": [
    {
      "rule_id": "rule-1",
      "associated_tools": ["tool_C"]
    }
  ]
}
```

This is not a json block.

```python
print("hello")
```
"""
        with open(self.agents_md_path, "w") as f:
            f.write(agents_md_content)

        # --- Create Mock Log File ---
        self.log_path = os.path.join(self.test_dir, "activity.log.jsonl")
        log_entries = [
            {"action": {"type": "TOOL_EXEC", "details": {"command": "tool_A --arg"}}},
            {"action": {"type": "TOOL_EXEC", "details": {"command": "python3 tooling/script.py"}}},
            {"action": {"type": "FILE_WRITE", "details": {}}},
            {"action": {"type": "TOOL_EXEC", "details": {"command": "tool_D"}}}, # Unreferenced tool
            {"action": {"type": "TOOL_EXEC", "details": {"command": "tool_A"}}}, # Repeated tool
        ]
        with open(self.log_path, "w") as f:
            for entry in log_entries:
                f.write(json.dumps(entry) + "\n")
            f.write("this is not a valid json line\n") # Add malformed line

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_get_protocol_tools(self):
        """Verify that tools are correctly extracted from AGENTS.md."""
        expected_tools = {"tool_A", "tool_B", "tool_C"}
        protocol_tools = get_protocol_tools_from_agents_md(self.agents_md_path)
        self.assertEqual(protocol_tools, expected_tools)

    def test_get_used_tools(self):
        """Verify that used tools are correctly parsed from the log file."""
        expected_tools = ["tool_A", "tooling/script.py", "tool_D", "tool_A"]
        used_tools = get_used_tools_from_log(self.log_path)
        self.assertEqual(used_tools, expected_tools)

    def test_completeness_check(self):
        """Verify the completeness check correctly identifies gaps."""
        protocol_tools = {"tool_A", "tool_B", "tool_C"}
        used_tools = ["tool_A", "tooling/script.py", "tool_D"]

        unreferenced, unused = run_completeness_check(used_tools, protocol_tools)

        self.assertEqual(set(unreferenced), {"tooling/script.py", "tool_D"})
        self.assertEqual(set(unused), {"tool_B", "tool_C"})

    def test_centrality_analysis(self):
        """Verify tool usage frequency is correctly calculated."""
        used_tools = ["tool_A", "tooling/script.py", "tool_D", "tool_A"]
        analysis = run_centrality_analysis(used_tools)
        self.assertEqual(analysis["tool_A"], 2)
        self.assertEqual(analysis["tooling/script.py"], 1)
        self.assertEqual(analysis["tool_D"], 1)

    def test_markdown_report_generation(self):
        """Verify the markdown report is generated with correct information."""
        source_check = {"status": "success", "message": "Up-to-date."}
        unreferenced = ["tool_D"]
        unused = ["tool_B"]
        centrality = run_centrality_analysis(["tool_A", "tool_D"])

        report = generate_markdown_report(source_check, unreferenced, unused, centrality)

        self.assertIn("# Protocol Audit Report", report)
        self.assertIn("- ✅ **Success:** Up-to-date.", report)
        self.assertIn("`tool_D`", report)
        self.assertIn("`tool_B`", report)
        self.assertIn("| `tool_A` | 1 |", report)

if __name__ == "__main__":
    unittest.main()