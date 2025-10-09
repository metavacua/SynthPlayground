import json
import os
from collections import Counter
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(ROOT_DIR, "tool_demonstration_log.txt")
AGENTS_FILE = os.path.join(ROOT_DIR, "AGENTS.md")


def get_used_tools_from_log(log_path):
    """Parses the log file to get a list of used tools."""
    try:
        with open(log_path, "r") as f:
            # Read all lines, strip whitespace, and filter out empty lines
            tools = [line.strip() for line in f if line.strip()]
        return tools
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_path}")
        return []


def get_protocol_tools_from_agents_md(agents_md_path):
    """Parses AGENTS.md to get a set of all tools associated with protocols."""
    try:
        with open(agents_md_path, "r") as f:
            content = f.read()

        # Extract content from the json code block
        start_marker = "```json\\n"
        end_marker = "\\n```"
        match = re.search(f"{start_marker}(.*?){end_marker}", content, re.DOTALL)

        if not match:
            print(f"Error: Could not find JSON block in {agents_md_path}")
            return set()

        json_content = match.group(1)
        data = json.loads(json_content)

        protocol_tools = set()
        for protocol in data.get("protocols", []):
            for tool in protocol.get("associated_tools", []):
                protocol_tools.add(tool)
        return protocol_tools

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing {agents_md_path}: {e}")
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


def main():
    """Main function to run the protocol auditor."""
    print("--- Initializing Protocol Auditor ---")

    # Get data from sources
    used_tools_from_log = get_used_tools_from_log(LOG_FILE)
    protocol_tools_from_agents = get_protocol_tools_from_agents_md(AGENTS_FILE)

    # Run analyses
    run_completeness_check(used_tools_from_log, protocol_tools_from_agents)
    run_centrality_analysis(used_tools_from_log)

    print("\\n--- Audit Complete ---")


if __name__ == "__main__":
    main()