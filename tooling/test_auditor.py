import unittest
import os
import json
import shutil
import datetime
from unittest.mock import patch

from tooling.auditor import run_plan_audit, run_docs_audit, run_health_audit

class TestSimplifiedAuditor(unittest.TestCase):

    def setUp(self):
        self.test_dir = "temp_test_audit_dir"
        os.makedirs(os.path.join(self.test_dir, "knowledge_core"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "logs"), exist_ok=True)

        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_plan_audit_dead_link(self):
        # Setup
        plan_registry_path = os.path.join("knowledge_core", "plan_registry.json")
        with open(plan_registry_path, "w") as f:
            json.dump({"dead_plan": "non_existent_plan.txt"}, f)

        # Patch PLAN_REGISTRY_PATH to be our test_dir
        with patch("tooling.auditor.PLAN_REGISTRY_PATH", plan_registry_path):
            report = run_plan_audit()
        self.assertIn("- ⚠️ **Dead Links Found:** 1 entries point to non-existent files.", report)

    def test_docs_audit_missing_docstring(self):
        # Setup
        system_docs_path = os.path.join("knowledge_core", "SYSTEM_DOCUMENTATION.md")
        with open(system_docs_path, "w") as f:
            f.write("### `missing_doc.py`\n\n_No module-level docstring found._")

        with patch("tooling.auditor.SYSTEM_DOCS_PATH", system_docs_path):
            report = run_docs_audit()
        self.assertIn("- ⚠️ **Missing Docstrings:** 1 modules are missing a module-level docstring.", report)

    def test_health_audit_log_staleness(self):
        # Setup
        log_file_path = os.path.join("logs", "activity.log.jsonl")
        stale_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)).isoformat()
        with open(log_file_path, "w") as f:
            f.write(json.dumps({"timestamp": stale_time}) + "\n")

        with patch("tooling.auditor.LOG_FILE", log_file_path):
            report = run_health_audit()
        self.assertIn("- ❌ **Log Staleness Detected:** The last log entry is more than an hour old.", report)

if __name__ == "__main__":
    unittest.main()
