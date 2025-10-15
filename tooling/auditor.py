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
from collections import Counter
from datetime import datetime

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
PLAN_REGISTRY_PATH = os.path.join(ROOT_DIR, "knowledge_core", "plan_registry.json")
SYSTEM_DOCS_PATH = os.path.join(ROOT_DIR, "knowledge_core", "SYSTEM_DOCUMENTATION.md")
AGENTS_MD_FILENAME = "AGENTS.md"
SPECIAL_DIRS = ["protocols/security"] # from protocol_auditor.py

# --- Protocol Audit Logic ---

def find_all_agents_md_files(root_dir):
    agents_files = []
    special_paths = {os.path.join(root_dir, d) for d in SPECIAL_DIRS}
    for dirpath, _, filenames in os.walk(root_dir):
        is_special = any(os.path.commonpath([dirpath, special]) == special for special in special_paths)
        if is_special:
            continue
        if AGENTS_MD_FILENAME in filenames:
            agents_files.append(os.path.join(dirpath, AGENTS_MD_FILENAME))
    return agents_files

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
                        if pos == len(line): break
                        log_entry, pos = decoder.raw_decode(line, pos)
                        if log_entry.get("action", {}).get("type") == "TOOL_EXEC":
                            tool_name = log_entry.get("action", {}).get("details", {}).get("tool_name")
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
    report = ["## 1. Protocol Audit"]
    all_agents_files = find_all_agents_md_files(ROOT_DIR)

    # Source Check
    stale_files = []
    for agents_md_path in all_agents_files:
        module_dir = os.path.dirname(agents_md_path)
        protocols_dir = os.path.join(module_dir, "protocols")
        if not os.path.isdir(protocols_dir): continue
        try:
            agents_md_mtime = os.path.getmtime(agents_md_path)
            for root, _, files in os.walk(protocols_dir):
                for file in files:
                    if file.endswith((".json", ".md")):
                        path = os.path.join(root, file)
                        if os.path.getmtime(path) > agents_md_mtime:
                            stale_files.append(os.path.relpath(agents_md_path, ROOT_DIR))
                            raise StopIteration
        except StopIteration:
            continue
    if stale_files:
        report.append("- ⚠️ **Stale Artifacts:** The following `AGENTS.md` files may be out of date. Run the `agents` build target.")
        for file in stale_files:
            report.append(f"  - `{file}`")
    else:
        report.append("- ✅ **`AGENTS.md` Source Check:** All `AGENTS.md` files appear to be up-to-date.")

    # Completeness Check
    used_tools = get_used_tools_from_log(LOG_FILE)
    protocol_tools = get_protocol_tools_from_agents_md(all_agents_files)
    unreferenced = sorted(list(set(used_tools) - protocol_tools))
    unused = sorted(list(protocol_tools - set(used_tools)))

    report.append("\n### Protocol Completeness")
    if not unreferenced:
        report.append("- ✅ All used tools are referenced in a protocol.")
    else:
        report.append("- ⚠️ **Unreferenced Tools:** The following tools were used but are not in any protocol:")
        for tool in unreferenced: report.append(f"  - `{tool}`")

    if not unused:
        report.append("- ✅ All protocol tools have been used.")
    else:
        report.append("- ℹ️ **Unused Tools:** The following tools are in a protocol but were not used in the log:")
        for tool in unused: report.append(f"  - `{tool}`")

    # Centrality Analysis
    report.append("\n### Tool Centrality")
    if not used_tools:
        report.append("- ℹ️ No tool usage recorded in the log.")
    else:
        report.append("| Tool | Usage Count |")
        report.append("|------|-------------|")
        for tool, count in Counter(used_tools).most_common():
            report.append(f"| `{tool}` | {count} |")
    return report

# --- Plan Registry Audit Logic ---

def run_plan_registry_audit():
    report = ["## 2. Plan Registry Audit"]
    dead_links = []
    if not os.path.exists(PLAN_REGISTRY_PATH):
        report.append(f"- ❌ **Error:** Plan registry not found at `{PLAN_REGISTRY_PATH}`")
        return report
    try:
        with open(PLAN_REGISTRY_PATH, 'r') as f:
            registry = json.load(f)
        for name, path in registry.items():
            if not os.path.exists(os.path.join(ROOT_DIR, path)):
                dead_links.append((name, path))
    except json.JSONDecodeError:
        report.append(f"- ❌ **Error:** Could not decode JSON from `{PLAN_REGISTRY_PATH}`")
        return report

    if not dead_links:
        report.append("- ✅ **Success:** All registered plans are valid.")
    else:
        report.append(f"- ⚠️ **Dead Links Found:** {len(dead_links)} entries point to non-existent files.")
        for name, path in dead_links:
            report.append(f"  - `{name}` -> `{path}`")
    return report

# --- Documentation Audit Logic ---

def run_doc_audit():
    report = ["## 3. Documentation Audit"]
    missing_docstrings = []
    if not os.path.exists(SYSTEM_DOCS_PATH):
        report.append(f"- ❌ **Error:** System documentation not found at `{SYSTEM_DOCS_PATH}`. Run the `docs` build target first.")
        return report
    try:
        with open(SYSTEM_DOCS_PATH, "r") as f:
            content = f.read()
        pattern = re.compile(r"### `(.*?\.py)`\n\n_No module-level docstring found._")
        missing_docstrings = pattern.findall(content)
    except Exception as e:
        report.append(f"- ❌ **Error:** Could not read or parse system documentation: {e}")
        return report

    if not missing_docstrings:
        report.append("- ✅ **Success:** All Python modules are documented.")
    else:
        report.append(f"- ⚠️ **Missing Docstrings:** {len(missing_docstrings)} modules are missing a module-level docstring.")
        for module in missing_docstrings:
            report.append(f"  - `{module}`")
    return report

# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Unified repository audit tool.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "audit_type",
        nargs='?',
        default="all",
        choices=["all", "protocol", "plans", "docs"],
        help="The type of audit to run.\n"
             " - all: Run all audits.\n"
             " - protocol: Audit protocols, tool usage, and AGENTS.md freshness.\n"
             " - plans: Audit the plan registry for dead links.\n"
             " - docs: Audit for missing Python module docstrings."
    )
    args = parser.parse_args()

    print(f"--- Running Unified Auditor (Task: {args.audit_type.upper()}) ---", file=sys.stderr)

    report_parts = [f"# Unified Audit Report ({datetime.now().isoformat()})"]

    if args.audit_type in ["all", "protocol"]:
        report_parts.extend(run_protocol_audit())
    if args.audit_type in ["all", "plans"]:
        report_parts.extend(run_plan_registry_audit())
    if args.audit_type in ["all", "docs"]:
        report_parts.extend(run_doc_audit())

    report_content = "\n\n".join(report_parts)
    report_path = os.path.join(ROOT_DIR, "audit_report.md")
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"--- Audit Complete. Report generated at: {os.path.relpath(report_path, ROOT_DIR)} ---", file=sys.stderr)

if __name__ == "__main__":
    main()