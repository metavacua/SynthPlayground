"""
A simplified, direct auditing tool for the repository.
"""

import argparse
import datetime
import json
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
PLAN_REGISTRY_PATH = os.path.join(ROOT_DIR, "knowledge_core", "plan_registry.json")
SYSTEM_DOCS_PATH = os.path.join(ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md")

def run_plan_audit():
    """Runs the plan registry audit."""
    report = []
    if not os.path.exists(PLAN_REGISTRY_PATH):
        report.append("- ⚠️ **Plan Registry Not Found:** Could not find the plan registry.")
        return report

    with open(PLAN_REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    dead_links = []
    for name, path in registry.items():
        if not os.path.exists(os.path.join(ROOT_DIR, path)):
            dead_links.append((name, path))

    if dead_links:
        report.append(f"- ⚠️ **Dead Links Found:** {len(dead_links)} entries point to non-existent files.")
        for name, path in dead_links:
            report.append(f"  - `{name}` -> `{path}`")
    else:
        report.append("- ✅ **Success:** All registered plans are valid.")
    return report

def run_docs_audit():
    """Runs the documentation audit."""
    report = []
    if not os.path.exists(SYSTEM_DOCS_PATH):
        report.append("- ⚠️ **System Documentation Not Found:** Could not find the system documentation.")
        return report

    with open(SYSTEM_DOCS_PATH, "r") as f:
        content = f.read()

    missing_docstrings = re.findall(r"### `(.*?)`\n\n_No module-level docstring found._", content)

    if missing_docstrings:
        report.append(f"- ⚠️ **Missing Docstrings:** {len(missing_docstrings)} modules are missing a module-level docstring.")
        for module in missing_docstrings:
            report.append(f"  - `{module}`")
    else:
        report.append("- ✅ **Success:** All modules have docstrings.")
    return report

def run_health_audit():
    """Runs the system health audit."""
    report = []
    if not os.path.exists(LOG_FILE):
        report.append("- ❌ **Log File Not Found:** The agent's activity log is missing.")
        return report

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        report.append("- ❌ **Log File is Empty:** The agent's activity log is empty.")
        return report

    last_log = json.loads(lines[-1])
    last_timestamp = datetime.datetime.fromisoformat(last_log["timestamp"])

    if last_timestamp < datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1):
        report.append("- ❌ **Log Staleness Detected:** The last log entry is more than an hour old.")
    else:
        report.append("- ✅ **Success:** Log file is up-to-date.")
    return report

def main():
    parser = argparse.ArgumentParser(description="Simplified repository auditing tool.")
    parser.add_argument(
        "task",
        nargs="?",
        default="all",
        choices=["all", "plans", "docs", "health"],
        help="The audit task to run.",
    )
    args = parser.parse_args()

    print("--- Running Simplified Auditor ---")

    report_content = f"# Simplified Audit Report ({datetime.datetime.now(datetime.timezone.utc).isoformat()})\n\n"

    audit_functions = {
        "plans": ("Plan Registry Audit", run_plan_audit),
        "docs": ("Documentation Audit", run_docs_audit),
        "health": ("System Health Audit", run_health_audit),
    }

    tasks_to_run = audit_functions.keys() if args.task == 'all' else [args.task]

    for task in tasks_to_run:
        title, audit_func = audit_functions[task]
        report_content += f"## {title}\n\n"
        content = "\n".join(audit_func())
        report_content += f"{content}\n\n"

    with open("audit_report.md", "w") as f:
        f.write(report_content)

    print("--- Audit Complete. Report generated at: audit_report.md ---")

if __name__ == "__main__":
    main()
