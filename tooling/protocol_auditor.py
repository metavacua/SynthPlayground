"""
Audits the agent's behavior against its governing protocols and generates a report.

This script performs a comprehensive analysis to ensure the agent's actions,
as recorded in the activity log, align with the defined protocols in AGENTS.md.
It serves as a critical feedback mechanism for maintaining operational integrity.
The final output is a detailed `audit_report.md` file.

The auditor performs three main checks:
1.  **`AGENTS.md` Source Check:** Verifies if the `AGENTS.md` build artifact is
    potentially stale by comparing its modification time against the source
    protocol files in the `protocols/` directory.
2.  **Protocol Completeness:** It cross-references the tools used in the log
    (`logs/activity.log.jsonl`) against the tools defined in `AGENTS.md` to find:
    - Tools used but not associated with any formal protocol.
    - Tools defined in protocols but never used in the log.
3.  **Tool Centrality:** It conducts a frequency analysis of tool usage to
    identify which tools are most critical to the agent's workflow.

The script parses all embedded JSON protocol blocks within `AGENTS.md` and reads
from the standard `logs/activity.log.jsonl` log file, providing a reliable and
accurate audit.
"""
import json
import os
import sys
from collections import Counter
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
AGENTS_MD_FILENAME = "AGENTS.md"


def find_all_agents_md_files(root_dir):
    """Finds all AGENTS.md files in the repository."""
    agents_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if AGENTS_MD_FILENAME in filenames:
            agents_files.append(os.path.join(dirpath, AGENTS_MD_FILENAME))
    return agents_files


def get_used_tools_from_log(log_path):
    """
    Parses the JSONL log file to get a list of used tool names.
    It specifically looks for 'TOOL_EXEC' actions and extracts the tool
    from the 'command' field based on the logging schema.
    This version is robust against malformed lines with multiple JSON objects.
    """
    used_tools = []
    decoder = json.JSONDecoder()
    try:
        with open(log_path, "r") as f:
            for line in f:
                line = line.strip()
                pos = 0
                while pos < len(line):
                    try:
                        # Skip leading whitespace to find the start of the next potential object
                        while pos < len(line) and line[pos].isspace():
                            pos += 1
                        if pos == len(line):
                            break

                        log_entry, pos = decoder.raw_decode(line, pos)
                        action = log_entry.get("action", {})
                        if action.get("type") == "TOOL_EXEC":
                            details = action.get("details", {})
                            tool_name = details.get("tool_name")
                            if tool_name:
                                # The modern schema provides the tool name directly.
                                # No more parsing from a 'command' string is needed.
                                used_tools.append(tool_name)
                    except json.JSONDecodeError:
                        # If raw_decode fails, we assume the rest of the line is not valid JSON.
                        # We only print a warning if the line seemed to start with a JSON-like character.
                        if line[pos:].lstrip().startswith(('{', '[')):
                            print(f"Warning: Skipping malformed or unexpected entry in log: {line}", file=sys.stderr)
                        break  # Move to the next line
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}", file=sys.stderr)
    return used_tools


def get_protocol_tools_from_agents_md(agents_md_paths):
    """
    Parses a list of AGENTS.md files to get a set of all tools associated
    with protocols.
    """
    protocol_tools = set()
    for file_path in agents_md_paths:
        try:
            with open(file_path, "r") as f:
                content = f.read()

            json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
            if not json_blocks:
                print(f"Warning: No JSON blocks found in {file_path}", file=sys.stderr)
                continue

            for json_content in json_blocks:
                try:
                    data = json.loads(json_content)
                    rules = data.get("rules", [])
                    for tool in data.get("associated_tools", []):
                        protocol_tools.add(tool)
                    for rule in rules:
                        for tool in rule.get("associated_tools", []):
                            protocol_tools.add(tool)
                except json.JSONDecodeError:
                    continue
        except FileNotFoundError:
            print(f"Error: Protocol file not found at {file_path}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"An unexpected error occurred while parsing {file_path}: {e}", file=sys.stderr)
            continue
    return protocol_tools


def run_completeness_check(used_tools, protocol_tools):
    """Compares used tools with protocol-defined tools and returns the gaps."""
    used_tools_set = set(used_tools)
    unreferenced_tools = used_tools_set - protocol_tools
    unused_protocol_tools = protocol_tools - used_tools_set
    return sorted(list(unreferenced_tools)), sorted(list(unused_protocol_tools))


def run_centrality_analysis(used_tools):
    """Performs a frequency analysis on the tool log and returns the counts."""
    if not used_tools:
        return None
    return Counter(used_tools)


def run_protocol_source_check(all_agents_files):
    """
    Checks if each AGENTS.md file is older than its corresponding source files.
    Returns a list of warning/error dictionaries.
    """
    results = []
    for agents_md_path in all_agents_files:
        module_dir = os.path.dirname(agents_md_path)
        protocols_dir = os.path.join(module_dir, "protocols")

        if not os.path.isdir(protocols_dir):
            # This AGENTS.md file is likely a leaf or not a module, which is fine.
            continue

        try:
            agents_md_mtime = os.path.getmtime(agents_md_path)
            latest_source_mtime = 0
            latest_source_file = ""

            for root, _, files in os.walk(protocols_dir):
                for file in files:
                    if file.endswith((".json", ".md")):
                        path = os.path.join(root, file)
                        mtime = os.path.getmtime(path)
                        if mtime > latest_source_mtime:
                            latest_source_mtime = mtime
                            latest_source_file = path

            if latest_source_mtime > agents_md_mtime:
                results.append({
                    "status": "warning",
                    "message": f"`{os.path.relpath(agents_md_path, ROOT_DIR)}` may be out of date.",
                    "details": f"Latest source file modified: `{os.path.relpath(latest_source_file, ROOT_DIR)}`."
                })

        except Exception as e:
            results.append({
                "status": "error",
                "message": f"Could not perform source check for `{os.path.relpath(agents_md_path, ROOT_DIR)}`: {e}"
            })

    if not results:
        return [{"status": "success", "message": "All AGENTS.md files appear to be up-to-date."}]

    return results


def generate_markdown_report(source_checks, unreferenced, unused, centrality):
    """Generates a Markdown-formatted string from the audit results."""
    report = ["# Protocol Audit Report"]

    # --- Source Check ---
    report.append("## 1. `AGENTS.md` Source Check")
    has_warning = any(check['status'] == 'warning' for check in source_checks)
    has_error = any(check['status'] == 'error' for check in source_checks)

    if not has_warning and not has_error:
        report.append("- ✅ **Success:** All AGENTS.md files appear to be up-to-date.")
    else:
        for check in source_checks:
            if check['status'] == 'warning':
                report.append(f"- ⚠️ **Warning:** {check['message']}")
                report.append(f"  - {check['details']}")
                report.append("  - **Recommendation:** Run `make AGENTS.md` to re-compile.")
            elif check['status'] == 'error':
                 report.append(f"- ❌ **Error:** {check['message']}")


    # --- Completeness Check ---
    report.append("\n## 2. Protocol Completeness")
    report.append("### Tools Used But Not In Protocol")
    if not unreferenced:
        report.append("- ✅ All tools used are associated with a protocol.")
    else:
        report.append("- ⚠️ The following tools were used but are **not** associated with any protocol:")
        for tool in unreferenced:
            report.append(f"  - `{tool}`")

    report.append("\n### Tools In Protocol But Not Used")
    if not unused:
        report.append("- ✅ All tools associated with a protocol were used in the log.")
    else:
        report.append("- ℹ️ The following tools are associated with a protocol but were **not** used in the log:")
        for tool in unused:
            report.append(f"  - `{tool}`")

    # --- Centrality Analysis ---
    report.append("\n## 3. Tool Centrality Analysis")
    if not centrality:
        report.append("- ℹ️ No tool usage was recorded in the log.")
    else:
        report.append("Frequency of tool usage:")
        report.append("| Tool | Usage Count |")
        report.append("|------|-------------|")
        for tool, count in centrality.most_common():
            report.append(f"| `{tool}` | {count} |")

    return "\n".join(report)


def main():
    """Main function to run the protocol auditor and generate a report."""
    print("--- Initializing Protocol Auditor ---", file=sys.stderr)

    # Get data from sources
    all_agents_files = find_all_agents_md_files(ROOT_DIR)
    used_tools_from_log = get_used_tools_from_log(LOG_FILE)
    protocol_tools_from_agents = get_protocol_tools_from_agents_md(all_agents_files)

    # Run analyses
    source_check_results = run_protocol_source_check(all_agents_files)
    unreferenced_tools, unused_protocol_tools = run_completeness_check(used_tools_from_log, protocol_tools_from_agents)
    centrality_analysis = run_centrality_analysis(used_tools_from_log)

    # Generate report
    report_content = generate_markdown_report(
        source_check_results,
        unreferenced_tools,
        unused_protocol_tools,
        centrality_analysis
    )

    report_path = os.path.join(ROOT_DIR, "audit_report.md")
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"--- Audit Complete. Report generated at: {report_path} ---", file=sys.stderr)


if __name__ == "__main__":
    main()