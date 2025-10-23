import unittest
import os
import json
from unittest.mock import patch, mock_open
from tooling.auditor import (
    run_protocol_audit,
    run_plan_registry_audit,
    run_doc_audit,
    run_health_audit,
)
import datetime


class TestUnifiedAuditor(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_audit_dir"
        os.makedirs(os.path.join(self.test_dir, "protocols"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "knowledge_core"), exist_ok=True)

        self.agents_md = os.path.join(self.test_dir, "AGENTS.md")
        self.protocol_json = os.path.join(
            self.test_dir, "protocols", "test.protocol.json"
        )
        self.plan_registry = os.path.join(
            self.test_dir, "knowledge_core", "plan_registry.json"
        )
        self.system_docs = os.path.join(
            self.test_dir, "knowledge_core", "SYSTEM_DOCUMENTATION.md"
        )
        self.log_file = os.path.join(self.test_dir, "logs", "activity.log.jsonl")
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.test_dir)

    @patch(
        "tooling.auditor.ROOT_DIR", new_callable=lambda: os.getcwd() + "/test_audit_dir"
    )
    @patch(
        "tooling.auditor.LOG_FILE",
        new_callable=lambda: os.getcwd() + "/test_audit_dir/logs/activity.log.jsonl",
    )
    def test_protocol_audit(self, mock_root, mock_log):
        with open(self.protocol_json, "w") as f:
            json.dump(
                {"protocol_id": "test-proto-001", "associated_tools": ["test_tool"]}, f
            )
        with open(self.agents_md, "w") as f:
            f.write(
                '```json\n{"protocol_id": "test-proto-001", "associated_tools": ["test_tool"]}\n```'
            )
        with open(self.log_file, "w") as f:
            f.write(
                '{"action": {"type": "TOOL_EXEC", "details": {"tool_name": "test_tool"}}}\n'
            )

        report = run_protocol_audit()
        self.assertIn("## 1. Protocol Audit", report)
        self.assertIn("- ✅ **`AGENTS.md` Source Check:**", report[1])

    @patch(
        "tooling.auditor.PLAN_REGISTRY_PATH",
        new_callable=lambda: os.getcwd()
        + "/test_audit_dir/knowledge_core/plan_registry.json",
    )
    def test_plan_registry_audit(self, mock_path):
        with open(self.plan_registry, "w") as f:
            json.dump(
                {"valid_plan": "README.md", "invalid_plan": "non_existent_file.txt"}, f
            )

        report = run_plan_registry_audit()
        self.assertIn("## 2. Plan Registry Audit", report)
        self.assertIn(
            "⚠️ **Dead Links Found:** 1 entries point to non-existent files.", report[1]
        )

    @patch(
        "tooling.auditor.SYSTEM_DOCS_PATH",
        new_callable=lambda: os.getcwd()
        + "/test_audit_dir/knowledge_core/SYSTEM_DOCUMENTATION.md",
    )
    def test_doc_audit(self, mock_path):
        with open(self.system_docs, "w") as f:
            f.write("### `module/missing_doc.py`\n\n_No module-level docstring found._")

        report = run_doc_audit()
        self.assertIn("## 3. Documentation Audit", report)
        self.assertIn(
            "⚠️ **Missing Docstrings:** 1 modules are missing a module-level docstring.",
            report[1],
        )


if __name__ == "__main__":
    unittest.main()


class TestHealthAuditor(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_health_audit_dir"
        os.makedirs(os.path.join(self.test_dir, "logs"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "postmortems"), exist_ok=True)

        self.log_file = os.path.join(self.test_dir, "logs", "activity.log.jsonl")
        self.postmortem_file = os.path.join(
            self.test_dir, "postmortems", "2025-10-21-test-task.md"
        )
        self.session_start_time = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(minutes=10)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.test_dir)

    @patch(
        "tooling.auditor.LOG_FILE",
        new_callable=lambda: os.getcwd()
        + "/test_health_audit_dir/logs/activity.log.jsonl",
    )
    @patch(
        "tooling.auditor.POSTMORTEM_DIR",
        new_callable=lambda: os.getcwd() + "/test_health_audit_dir/postmortems",
    )
    def test_log_staleness(self, mock_postmortem_dir, mock_log_file):
        # Create a log file where the most recent entry is older than the session start time
        stale_time = (
            self.session_start_time - datetime.timedelta(minutes=5)
        ).isoformat()
        with open(self.log_file, "w") as f:
            log_entry = {
                "timestamp": stale_time,
                "action": {"type": "TOOL_EXEC", "details": {"tool_name": "test"}},
                "outcome": {"status": "SUCCESS"},
            }
            f.write(json.dumps(log_entry) + "\n")

        report = run_health_audit(self.session_start_time.isoformat())
        self.assertIn("❌ **Log Staleness Detected:**", report)

    @patch(
        "tooling.auditor.LOG_FILE",
        new_callable=lambda: os.getcwd()
        + "/test_health_audit_dir/logs/activity.log.jsonl",
    )
    @patch(
        "tooling.auditor.POSTMORTEM_DIR",
        new_callable=lambda: os.getcwd() + "/test_health_audit_dir/postmortems",
    )
    def test_success_only_tasks(self, mock_postmortem_dir, mock_log_file):
        # Create a log file with only success entries since the session start
        fresh_time = (
            self.session_start_time + datetime.timedelta(minutes=1)
        ).isoformat()
        with open(self.log_file, "w") as f:
            # The threshold is 5, so we need more than 5 actions for the same task.
            for i in range(6):
                log_entry = {
                    "task_id": "suspicious-task",
                    "timestamp": fresh_time,
                    "action": {"type": "TOOL_EXEC", "details": {"tool_name": f"test_{i}"}},
                    "outcome": {"status": "SUCCESS"},
                }
                f.write(json.dumps(log_entry) + "\n")

        report = run_health_audit(self.session_start_time.isoformat())
        self.assertIn("⚠️ **Success-Only Task Logs:**", report)

    @patch(
        "tooling.auditor.LOG_FILE",
        new_callable=lambda: os.getcwd()
        + "/test_health_audit_dir/logs/activity.log.jsonl",
    )
    @patch(
        "tooling.auditor.POSTMORTEM_DIR",
        new_callable=lambda: os.getcwd() + "/test_health_audit_dir/postmortems",
    )
    def test_incomplete_post_mortems(self, mock_postmortem_dir, mock_log_file):
        # Create a log file indicating a failure
        fresh_time = (
            self.session_start_time + datetime.timedelta(minutes=1)
        ).isoformat()
        with open(self.log_file, "w") as f:
            log_entry = {
                "task_id": "test-task",
                "timestamp": fresh_time,
                "action": {"type": "SYSTEM_FAILURE"},
                "outcome": {"status": "FAILURE"},
            }
            f.write(json.dumps(log_entry) + "\n")

        # Create an empty post-mortem file
        with open(self.postmortem_file, "w") as f:
            f.write("")  # Empty file

        report = run_health_audit(self.session_start_time.isoformat())
        self.assertIn("❌ **Incomplete Post-Mortems Detected:**", report)

    @patch(
        "tooling.auditor.LOG_FILE",
        new_callable=lambda: os.getcwd()
        + "/test_health_audit_dir/logs/activity.log.jsonl",
    )
    @patch(
        "tooling.auditor.POSTMORTEM_DIR",
        new_callable=lambda: os.getcwd() + "/test_health_audit_dir/postmortems",
    )
    def test_no_issues(self, mock_postmortem_dir, mock_log_file):
        # Create a healthy log file
        fresh_time = (
            self.session_start_time + datetime.timedelta(minutes=1)
        ).isoformat()
        with open(self.log_file, "w") as f:
            log_entry_success = {
                "task_id": "test-task",
                "timestamp": fresh_time,
                "action": {"type": "TOOL_EXEC"},
                "outcome": {"status": "SUCCESS"},
            }
            log_entry_failure = {
                "task_id": "test-task",
                "timestamp": fresh_time,
                "action": {"type": "TOOL_EXEC"},
                "outcome": {"status": "FAILURE"},
            }
            f.write(json.dumps(log_entry_success) + "\n")
            f.write(json.dumps(log_entry_failure) + "\n")

        # Create a complete post-mortem file for the failed task
        with open(self.postmortem_file, "w") as f:
            f.write("# Post-Mortem\nThis is a complete post-mortem.")

        report = run_health_audit(self.session_start_time.isoformat())
        self.assertIn("✅ **No new critical or warning level issues found.**", report)
