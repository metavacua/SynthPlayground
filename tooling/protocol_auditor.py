"""
Audits the agent's behavior against its governing protocols.

This script performs a comparative analysis between the tools defined in the
`AGENTS.md` protocol document and the tools actually used, as recorded in the
activity log. Its purpose is to provide a feedback loop for protocol enforcement
and to identify potential gaps or inconsistencies in the agent's behavior.

The auditor currently performs two main checks:
1.  **Protocol Completeness:** It identifies:
    - Tools that were used but are not associated with any formal protocol.
    - Tools that are defined in the protocols but were never used.
2.  **Tool Centrality:** It conducts a frequency analysis of the tools used,
    helping to identify which tools are most critical to the agent's workflow.
"""
import json
import os
import sys
from collections import Counter
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
AGENTS_FILE = os.path.join(ROOT_DIR, "AGENTS.md")


def get_used_tools_from_log(log_path):
    """
    Parses the JSONL log file to get a list of used tool names.
    It specifically looks for 'TOOL_EXEC' actions and extracts the tool
    from the 'command' field based on the logging schema.
    """
    used_tools = []
    try:
        with open(log_path, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    action = log_entry.get("action", {})
                    if action.get("type") == "TOOL_EXEC":
                        command = action.get("details", {}).get("command")
                        if not command:
                            continue

                        parts = command.split()
                        # Handle python scripts explicitly: "python3 tooling/script.py ..."
                        if len(parts) > 1 and parts[0].startswith("python") and parts[1].endswith(".py"):
                            tool_name = parts[1]
                        else:
                            # Handle other tools like "create_file_with_block(...)" or "grep 'pattern'"
                            tool_name = command.split('(')[0].split()[0]

                        used_tools.append(tool_name)

                except (json.JSONDecodeError, IndexError):
                    # This can happen with malformed logs or empty command strings
                    print(f"Warning: Skipping malformed or unexpected entry in log: {line.strip()}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}", file=sys.stderr)
    return used_tools


def get_protocol_tools_from_agents_md(agents_md_path):
    """
    Parses AGENTS.md to get a set of all tools associated with protocols.
    NOTE: This function correctly parses all JSON blocks, contrary to the
    outdated warning in the module-level docstring.
    """
    try:
        with open(agents_md_path, "r") as f:
            content = f.read()

        # Use re.findall to extract all JSON code blocks
        json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
        if not json_blocks:
            print(f"Warning: No JSON blocks found in {agents_md_path}", file=sys.stderr)
            return set()

        protocol_tools = set()
        for json_content in json_blocks:
            try:
                data = json.loads(json_content)
                # Handle both single protocol objects and lists of them
                rules = data.get("rules", [])
                # The associated_tools might be at the top level
                for tool in data.get("associated_tools", []):
                    protocol_tools.add(tool)
                # Or inside each rule
                for rule in rules:
                    for tool in rule.get("associated_tools", []):
                        protocol_tools.add(tool)
            except json.JSONDecodeError:
                # Ignore blocks that aren't valid JSON
                continue
        return protocol_tools

    except FileNotFoundError:
        print(f"Error: Protocol file not found at {agents_md_path}", file=sys.stderr)
        return set()
    except Exception as e:
        print(f"An unexpected error occurred while parsing {agents_md_path}: {e}", file=sys.stderr)
        return set()


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


def run_protocol_source_check():
    """
    Checks if AGENTS.md is older than its source files.
    Returns a dictionary with the check's status and relevant details.
    """
    agents_md_path = AGENTS_FILE
    protocols_dir = os.path.join(ROOT_DIR, "protocols")

    if not os.path.exists(agents_md_path):
        return {"status": "error", "message": "AGENTS.md not found."}

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
            return {
                "status": "warning",
                "message": "AGENTS.md may be out of date.",
                "details": f"Latest source file modified: `{latest_source_file}`."
            }
        else:
            return {"status": "success", "message": "AGENTS.md appears to be up-to-date."}

    except Exception as e:
        return {"status": "error", "message": f"Could not perform protocol source check: {e}"}


def generate_markdown_report(source_check, unreferenced, unused, centrality):
    """Generates a Markdown-formatted string from the audit results."""
    report = ["# Protocol Audit Report"]

    # --- Source Check ---
    report.append("## 1. `AGENTS.md` Source Check")
    if source_check['status'] == 'success':
        report.append(f"- ✅ **Success:** {source_check['message']}")
    elif source_check['status'] == 'warning':
        report.append(f"- ⚠️ **Warning:** {source_check['message']}")
        report.append(f"  - {source_check['details']}")
        report.append("  - **Recommendation:** Run `make AGENTS.md` to re-compile.")
    else:
        report.append(f"- ❌ **Error:** {source_check['message']}")

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
    used_tools_from_log = get_used_tools_from_log(LOG_FILE)
    protocol_tools_from_agents = get_protocol_tools_from_agents_md(AGENTS_FILE)

    # Run analyses
    source_check_result = run_protocol_source_check()
    unreferenced_tools, unused_protocol_tools = run_completeness_check(used_tools_from_log, protocol_tools_from_agents)
    centrality_analysis = run_centrality_analysis(used_tools_from_log)

    # Generate report
    report_content = generate_markdown_report(
        source_check_result,
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