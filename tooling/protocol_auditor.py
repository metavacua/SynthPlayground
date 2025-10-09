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

NOTE: The current implementation has known issues. It incorrectly parses the
`AGENTS.md` file by only reading the first JSON block and relies on a non-standard
log file. It requires modification to parse all JSON blocks and use the correct
`logs/activity.log.jsonl` file to be effective.
"""
import json
import os
from collections import Counter
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "activity.log.jsonl")
AGENTS_FILE = os.path.join(ROOT_DIR, "AGENTS.md")


def get_used_tools_from_log(log_path):
    """Parses the JSONL log file to get a list of used tools."""
    used_tools = []
    try:
        with open(log_path, "r") as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    # The tool name is nested within the action details
                    tool_name = log_entry.get("action", {}).get("details", {}).get("tool_name")
                    if tool_name:
                        used_tools.append(tool_name)
                except json.JSONDecodeError:
                    print(f"Warning: Skipping malformed JSON line in log: {line.strip()}")
                    continue
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}")
    return used_tools


def get_protocol_tools_from_agents_md(agents_md_path):
    """Parses AGENTS.md to get a set of all tools associated with protocols."""
    try:
        with open(agents_md_path, "r") as f:
            content = f.read()

        # Use re.findall to extract all JSON code blocks
        json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
        if not json_blocks:
            print(f"Warning: No JSON blocks found in {agents_md_path}")
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
        print(f"Error: Protocol file not found at {agents_md_path}")
        return set()
    except Exception as e:
        print(f"An unexpected error occurred while parsing {agents_md_path}: {e}")
        return set()


def run_completeness_check(used_tools, protocol_tools):
    """Compares used tools with protocol-defined tools and reports gaps."""
    print("--- Running Protocol Completeness Check ---")

    used_tools_set = set(used_tools)

    # Tools used in the log but not mentioned in any protocol
    unreferenced_tools = used_tools_set - protocol_tools

    # Tools mentioned in protocols but not used in the log
    unused_protocol_tools = protocol_tools - used_tools_set

    print("\\n[1] Analysis of Tool Usage vs. Protocol Association:")
    if not unreferenced_tools:
        print("  - Success: All tools used in the log are associated with a protocol.")
    else:
        print("  - Warning: The following tools were used but are NOT associated with any protocol:")
        for tool in sorted(list(unreferenced_tools)):
            print(f"    - {tool}")

    if not unused_protocol_tools:
        print("  - Success: All tools associated with a protocol were used in the log.")
    else:
        print("  - Info: The following tools are associated with a protocol but were NOT used in the log:")
        for tool in sorted(list(unused_protocol_tools)):
            print(f"    - {tool}")
    print("-" * 20)


def run_centrality_analysis(used_tools):
    """Performs a frequency analysis on the tool log."""
    print("\\n--- Running Tool Centrality Analysis ---")

    if not used_tools:
        print("  - No tools found in log to analyze.")
        return

    tool_counts = Counter(used_tools)

    print("\\n[2] Tool Usage Frequency:")
    # Sort by count descending, then alphabetically for ties
    for tool, count in tool_counts.most_common():
        print(f"  - {tool}: {count} time(s)")
    print("-" * 20)


def run_protocol_source_check():
    """Checks if AGENTS.md is older than its source files."""
    print("\\n--- Running Protocol Source Check ---")
    agents_md_path = AGENTS_FILE
    protocols_dir = os.path.join(ROOT_DIR, "protocols")

    if not os.path.exists(agents_md_path):
        print("  - Warning: AGENTS.md not found. Cannot perform source check.")
        return

    try:
        agents_md_mtime = os.path.getmtime(agents_md_path)

        # Find the most recently modified file in the protocols directory
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
            print(f"  - Warning: AGENTS.md may be out of date.")
            print(f"    - Latest source file modified: {latest_source_file}")
            print(f"    - Recommendation: Run 'make AGENTS.md' to re-compile.")
        else:
            print("  - Success: AGENTS.md appears to be up-to-date with its sources.")

    except Exception as e:
        print(f"  - Error: Could not perform protocol source check. {e}")
    print("-" * 20)


def main():
    """Main function to run the protocol auditor."""
    print("--- Initializing Protocol Auditor ---")

    # Get data from sources
    used_tools_from_log = get_used_tools_from_log(LOG_FILE)
    protocol_tools_from_agents = get_protocol_tools_from_agents_md(AGENTS_FILE)

    # Run analyses
    run_protocol_source_check()
    run_completeness_check(used_tools_from_log, protocol_tools_from_agents)
    run_centrality_analysis(used_tools_from_log)

    print("\\n--- Audit Complete ---")


if __name__ == "__main__":
    main()