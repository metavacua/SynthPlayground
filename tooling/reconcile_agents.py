import argparse
import os
import re
from collections import OrderedDict

def load_archived_agents(input_dir: str) -> dict:
    """
    Scans the archive directory, reads each agent file, and returns a dictionary
    mapping the sanitized branch name to its content.
    """
    archived_agents = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(("_AGENTS.md", "_agent.md")):
            # Extract the original branch name from the filename
            # e.g., "feat_new-feature_AGENTS.md" -> "feat_new-feature"
            match = re.match(r"(.+?)_AGENTS\.md|(.+?)_agent\.md", filename)
            if match:
                # Determine which group was matched
                branch_name = match.group(1) or match.group(2)
                filepath = os.path.join(input_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    archived_agents[branch_name] = f.read()
    print(f"Loaded {len(archived_agents)} agent files from '{input_dir}'.")
    return archived_agents

def parse_agent_md(content: str) -> OrderedDict:
    """
    Parses the string content of an AGENTS.md file into a dictionary,
    splitting it by markdown headers.
    """
    # Use OrderedDict to preserve the order of sections
    sections = OrderedDict()
    # Regex to find markdown headers (##, ###, etc.)
    header_pattern = re.compile(r"^(## .*)$", re.MULTILINE)

    # Find all headers
    headers = list(header_pattern.finditer(content))

    # Preamble: content before the first header
    preamble_end = headers[0].start() if headers else len(content)
    preamble = content[:preamble_end].strip()
    if preamble:
        sections["Preamble"] = preamble

    # Extract content for each section
    for i, header_match in enumerate(headers):
        header_text = header_match.group(1).strip()
        start_pos = header_match.end()
        # End position is the start of the next header, or end of the file
        end_pos = headers[i + 1].start() if i + 1 < len(headers) else len(content)
        section_content = content[start_pos:end_pos].strip()
        sections[header_text] = section_content

    return sections

def reconcile_versions(parsed_agents: dict, base_branch: str) -> (OrderedDict, str):
    """
    Reconciles different versions of parsed AGENTS.md files.

    Args:
        parsed_agents: A dictionary of parsed agent files.
        base_branch: The name of the branch to use as the base for reconciliation.

    Returns:
        A tuple containing the reconciled data (OrderedDict) and a report string.
    """
    if base_branch not in parsed_agents:
        raise ValueError(f"Base branch '{base_branch}' not found in the parsed agents data.")

    # Initialize with the base branch content
    reconciled_data = parsed_agents[base_branch].copy()
    report_lines = [f"# Reconciliation Report\n\nBase Branch: `{base_branch}`\n"]

    # Iterate through every other branch to compare and merge
    for branch_name, parsed_content in parsed_agents.items():
        if branch_name == base_branch:
            continue

        report_lines.append(f"\n---\n\n## Comparing with Branch: `{branch_name}`\n")

        # Check for new or conflicting sections
        for section, content in parsed_content.items():
            if section not in reconciled_data:
                # New section found, add it
                reconciled_data[section] = content
                report_lines.append(f"* **New Section Added**: `{section}`")
            elif reconciled_data[section] != content:
                # Conflict detected
                report_lines.append(f"* **Conflict Detected**: `{section}`")

                # Append the conflicting version with markers
                conflict_block = (
                    f"\n\n<<<<<<< Current (Reconciled from previous steps)\n"
                    f"{reconciled_data[section]}\n"
                    f"=======\n"
                    f"Content from branch: {branch_name}\n"
                    f"{content}\n"
                    f">>>>>>> End of conflict from {branch_name}\n"
                )
                reconciled_data[section] += conflict_block
            else:
                # Identical section, do nothing
                report_lines.append(f"* **Identical Section**: `{section}` (No action taken)")

    return reconciled_data, "\n".join(report_lines)


def generate_reconciled_md(reconciled_data: OrderedDict, output_path: str):
    """Writes the reconciled data to a markdown file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for section, content in reconciled_data.items():
            # The "Preamble" doesn't have a header itself
            if section == "Preamble":
                f.write(content + "\n\n")
            else:
                f.write(f"{section}\n\n{content}\n\n")
    print(f"Successfully generated reconciled file: '{output_path}'")

def write_report(report_content: str, report_path: str):
    """Writes the reconciliation report to a file."""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Successfully generated reconciliation report: '{report_path}'")


def main():
    parser = argparse.ArgumentParser(
        description="Reconciles multiple versions of AGENTS.md from an archive."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing the archived AGENTS.md files.",
    )
    parser.add_argument(
        "--output-file",
        default="AGENTS.md.reconciled",
        help="Path to write the reconciled AGENTS.md file.",
    )
    parser.add_argument(
        "--report-file",
        default="reconciliation_report.md",
        help="Path to write the reconciliation report.",
    )
    parser.add_argument(
        "--base-branch",
        default="main",
        help="The branch to use as the base for reconciliation.",
    )
    args = parser.parse_args()

    # 1. Load
    archived_agents = load_archived_agents(args.input_dir)

    # 2. Parse
    parsed_agents = {
        branch: parse_agent_md(content) for branch, content in archived_agents.items()
    }

    # 3. Reconcile
    try:
        reconciled_data, report_content = reconcile_versions(parsed_agents, args.base_branch)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # 4. Generate output files
    generate_reconciled_md(reconciled_data, args.output_file)
    write_report(report_content, args.report_file)

    print("\nReconciliation process complete.")

if __name__ == "__main__":
    main()