"""
A unified auditing tool for maintaining repository health and compliance.

This script combines the functionality of several disparate auditing tools into a
single, comprehensive command-line interface. It serves as the central tool for
validating the key components of the agent's architecture, including protocols,
plans, and documentation.

The auditor can perform the following checks:
1.  **Protocol Audit (`protocol`):**
    - Checks if `AGENTS.md` artifacts are stale compared to their source files.
    - Verifies protocol completeness by comparing tools used in logs against
      tools defined in protocols.
    - Analyzes tool usage frequency (centrality).
2.  **Plan Registry Audit (`plans`):**
    - Scans `knowledge_core/plan_registry.json` for "dead links" where the
      target plan file does not exist.
3.  **Documentation Audit (`docs`):**
    - Scans the generated `SYSTEM_DOCUMENTATION.md` to find Python modules
      that are missing module-level docstrings.

The tool is designed to be run from the command line and can execute specific
audits or all of them, generating a consolidated `audit_report.md` file.
"""

import json
import os
import sys
import re
import argparse
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tooling.auditor_logic import (
    analyze_protocol_completeness,
    analyze_tool_centrality,
    analyze_plan_registry,
    analyze_documentation,
    analyze_system_health,
)
from tooling.symbol_extractor import SymbolExtractor

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.file_system_utils import find_files

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
PLAN_REGISTRY_PATH = os.path.join(ROOT_DIR, "knowledge_core", "plan_registry.json")
SYSTEM_DOCS_PATH = os.path.join(ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md")
KNOWLEDGE_LESSONS_PATH = os.path.join(ROOT_DIR, "knowledge_core", "lessons.jsonl")
POSTMORTEM_DIR = os.path.join(ROOT_DIR, "postmortems")
AGENTS_MD_FILENAME = "AGENTS.md"
SPECIAL_DIRS = ["protocols/security"]  # from protocol_auditor.py


# --- Protocol Audit Logic ---


def find_all_agents_md_files(root_dir):
    return [os.path.join(root_dir, f) for f in find_files(AGENTS_MD_FILENAME, root_dir)]


def get_used_tools_from_log(log_path):
    used_tools = []
    decoder = json.JSONDecoder()
    try:
        with open(log_path, "r") as f:
            for line in f:
                line = line.strip()
                pos = 0
                while pos < len(line):
                    try:
                        while pos < len(line) and line[pos].isspace():
                            pos += 1
                        if pos == len(line):
                            break
                        log_entry, pos = decoder.raw_decode(line, pos)
                        if log_entry.get("action", {}).get("type") == "TOOL_EXEC":
                            tool_name = (
                                log_entry.get("action", {})
                                .get("details", {})
                                .get("tool_name")
                            )
                            if tool_name:
                                used_tools.append(tool_name)
                    except json.JSONDecodeError:
                        break
    except FileNotFoundError:
        print(f"Warning: Log file not found at {log_path}", file=sys.stderr)
    return used_tools


def get_protocol_tools_from_agents_md(agents_md_paths):
    protocol_tools = set()
    for file_path in agents_md_paths:
        try:
            with open(file_path, "r") as f:
                content = f.read()
            json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
            for json_content in json_blocks:
                try:
                    data = json.loads(json_content)
                    protocol_tools.update(data.get("associated_tools", []))
                    for rule in data.get("rules", []):
                        protocol_tools.update(rule.get("associated_tools", []))
                except json.JSONDecodeError:
                    continue
        except FileNotFoundError:
            print(f"Warning: Protocol file not found at {file_path}", file=sys.stderr)
    return protocol_tools


def run_protocol_audit():
    report = []
    all_agents_files = find_all_agents_md_files(ROOT_DIR)

    # Source Check
    stale_files = []
    for agents_md_path in all_agents_files:
        module_dir = os.path.dirname(agents_md_path)
        protocols_dir = os.path.join(module_dir, "protocols")
        if not os.path.isdir(protocols_dir):
            continue
        try:
            agents_md_mtime = os.path.getmtime(agents_md_path)
            protocol_files = find_files("*.json", protocols_dir) + find_files(
                "*.md", protocols_dir
            )
            for proto_file in protocol_files:
                path = os.path.join(ROOT_DIR, proto_file)
                if os.path.getmtime(path) > agents_md_mtime:
                    stale_files.append(os.path.relpath(agents_md_path, ROOT_DIR))
                    break
        except FileNotFoundError:
            # This can happen if a file is deleted during the audit
            continue
    if stale_files:
        report.append(
            "- ⚠️ **Stale Artifacts:** The following `AGENTS.md` files may be out of date. Run the `agents` build target."
        )
        for file in stale_files:
            report.append(f"  - `{file}`")
    else:
        report.append(
            "- ✅ **`AGENTS.md` Source Check:** All `AGENTS.md` files appear to be up-to-date."
        )

    # Completeness Check
    used_tools = get_used_tools_from_log(LOG_FILE)
    protocol_tools = get_protocol_tools_from_agents_md(all_agents_files)
    unreferenced, unused = analyze_protocol_completeness(used_tools, protocol_tools)

    report.append("\n### Protocol Completeness")
    if not unreferenced:
        report.append("- ✅ All used tools are referenced in a protocol.")
    else:
        report.append(
            "- ⚠️ **Unreferenced Tools:** The following tools were used but are not in any protocol:"
        )
        for tool in unreferenced:
            report.append(f"  - `{tool}`")

    if not unused:
        report.append("- ✅ All protocol tools have been used.")
    else:
        report.append(
            "- ℹ️ **Unused Tools:** The following tools are in a protocol but were not used in the log:"
        )
        for tool in unused:
            report.append(f"  - `{tool}`")

    # Centrality Analysis
    report.append("\n### Tool Centrality")
    centrality = analyze_tool_centrality(used_tools)
    if not centrality:
        report.append("- ℹ️ No tool usage recorded in the log.")
    else:
        report.append("| Tool | Usage Count |")
        report.append("|------|-------------|")
        for tool, count in centrality:
            report.append(f"| `{tool}` | {count} |")
    return report


# --- Plan Registry Audit Logic ---


def run_plan_registry_audit():
    report = []
    if not os.path.exists(PLAN_REGISTRY_PATH):
        report.append(
            f"- ❌ **Error:** Plan registry not found at `{PLAN_REGISTRY_PATH}`"
        )
        return report
    try:
        with open(PLAN_REGISTRY_PATH, "r") as f:
            registry = json.load(f)
        dead_links = analyze_plan_registry(registry, ROOT_DIR)
    except json.JSONDecodeError:
        report.append(
            f"- ❌ **Error:** Could not decode JSON from `{PLAN_REGISTRY_PATH}`"
        )
        return report

    if not dead_links:
        report.append("- ✅ **Success:** All registered plans are valid.")
    else:
        report.append(
            f"- ⚠️ **Dead Links Found:** {len(dead_links)} entries point to non-existent files."
        )
        for name, path in dead_links:
            report.append(f"  - `{name}` -> `{path}`")
    return report


# --- Documentation Audit Logic ---


def run_doc_audit():
    report = []
    if not os.path.exists(SYSTEM_DOCS_PATH):
        report.append(
            f"- ❌ **Error:** System documentation not found at `{SYSTEM_DOCS_PATH}`. Run the `docs` build target first."
        )
        return report
    try:
        with open(SYSTEM_DOCS_PATH, "r") as f:
            content = f.read()
        missing_docstrings = analyze_documentation(content)
    except Exception as e:
        report.append(
            f"- ❌ **Error:** Could not read or parse system documentation: {e}"
        )
        return report

    if not missing_docstrings:
        report.append("- ✅ **Success:** All Python modules are documented.")
    else:
        report.append(
            f"- ⚠️ **Missing Docstrings:** {len(missing_docstrings)} modules are missing a module-level docstring."
        )
        for module in missing_docstrings:
            report.append(f"  - `{module}`")
    return report


# --- System Health Audit Logic ---


def run_knowledge_audit():
    report = []
    if not os.path.exists(KNOWLEDGE_LESSONS_PATH):
        report.append(
            f"- ❌ **Error:** Knowledge base not found at `{KNOWLEDGE_LESSONS_PATH}`"
        )
        return report

    extractor = SymbolExtractor()
    dead_links = []
    with open(KNOWLEDGE_LESSONS_PATH, "r") as f:
        for line in f:
            try:
                lesson = json.loads(line)
                action = lesson.get("action", {})
                if action.get("command") == "placeholder":
                    continue  # Skip placeholder actions

                # This is a simplified check. A real implementation would
                # involve more sophisticated symbol analysis.
                params = action.get("parameters", {})
                for key, value in params.items():
                    if "symbol" in key or "file" in key:
                        references = extractor.find_all_references(value)
                        if not references:
                            dead_links.append(
                                {
                                    "lesson_id": lesson.get("lesson_id"),
                                    "symbol": value,
                                }
                            )
            except json.JSONDecodeError:
                continue

    if not dead_links:
        report.append("- ✅ **Success:** All knowledge base entries are valid.")
    else:
        report.append(
            f"- ⚠️ **Dead Links Found:** {len(dead_links)} knowledge entries point to non-existent symbols."
        )
        for link in dead_links:
            report.append(f"  - Lesson: `{link['lesson_id']}` -> Symbol: `{link['symbol']}`")
    return report


def run_health_audit(session_start_time_iso: str) -> list[str]:
    """
    Performs a system health audit, checking for "absence of evidence" anomalies.
    """
    if not os.path.exists(LOG_FILE):
        return ["- ❌ **Log Staleness Detected:** Log file not found. The agent's logging system may be broken."]

    with open(LOG_FILE, "r") as f:
        log_content = f.readlines()

    return analyze_system_health(
        log_content, POSTMORTEM_DIR, session_start_time_iso
    ).split('\n')


# --- Main ---


def main():
    parser = argparse.ArgumentParser(
        description="Unified repository audit tool.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "audit_type",
        nargs="?",
        default="all",
        choices=["all", "protocol", "plans", "docs", "health", "knowledge"],
        help="The type of audit to run.\n"
        " - all: Run all audits.\n"
        " - protocol: Audit protocols, tool usage, and AGENTS.md freshness.\n"
        " - plans: Audit the plan registry for dead links.\n"
        " - docs: Audit for missing Python module docstrings.\n"
        " - health: Audit system health for 'absence of evidence' anomalies.\n"
        " - knowledge: Audit the knowledge base for dead links.",
    )
    parser.add_argument("--session-start-time", help="The start time of the current session.", default=datetime.now().isoformat())
    args = parser.parse_args()

    print(
        f"--- Running Unified Auditor (Task: {args.audit_type.upper()}) ---",
        file=sys.stderr,
    )

    report_parts = [f"# Unified Audit Report ({datetime.now().isoformat()})"]

    audit_map = {
        "protocol": ("Protocol Audit", run_protocol_audit),
        "plans": ("Plan Registry Audit", run_plan_registry_audit),
        "docs": ("Documentation Audit", run_doc_audit),
        "knowledge": ("Knowledge Base Audit", run_knowledge_audit),
        "health": ("System Health Audit", lambda: run_health_audit(args.session_start_time)),
    }

    selected_audits = []
    if args.audit_type == "all":
        selected_audits = list(audit_map.keys())
    else:
        selected_audits = [args.audit_type]

    section_number = 1
    for audit_key in selected_audits:
        title, audit_func = audit_map[audit_key]
        content = audit_func()
        if content:
            report_parts.append(f"## {section_number}. {title}")
            report_parts.extend(content)
            section_number += 1

    report_content = "\n\n".join(report_parts)
    report_path = os.path.join(ROOT_DIR, "audit_report.md")
    with open(report_path, "w") as f:
        f.write(report_content)

    print(
        f"--- Audit Complete. Report generated at: {os.path.relpath(report_path, ROOT_DIR)} ---",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
