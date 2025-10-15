"""
A command-line tool for programmatically updating protocol source files.

This script provides the mechanism for the agent to perform self-correction
by modifying its own governing protocols based on structured, actionable
lessons. It is a key component of the Protocol-Driven Self-Correction (PDSC)
workflow.

The tool operates on the .protocol.json files located in the `protocols/`
directory, performing targeted updates based on command-line arguments.
"""

import argparse
import json
import os
import glob

DEFAULT_PROTOCOLS_DIR = "protocols/"


def find_protocol_file(protocol_id: str, protocols_dir: str) -> str | None:
    """Finds the protocol file path corresponding to a given protocol_id."""
    for filepath in glob.glob(os.path.join(protocols_dir, "*.protocol.json")):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                if data.get("protocol_id") == protocol_id:
                    return filepath
        except (json.JSONDecodeError, IOError):
            continue
    return None


def add_tool_to_protocol(protocol_id: str, tool_name: str, protocols_dir: str):
    """
    Adds a tool to the 'associated_tools' list of a specified protocol.
    """
    protocol_file = find_protocol_file(protocol_id, protocols_dir)
    if not protocol_file:
        print(
            f"Error: Protocol with ID '{protocol_id}' not found in '{protocols_dir}'."
        )
        # Exit with a non-zero status code to indicate failure to the calling process.
        exit(1)

    try:
        with open(protocol_file, "r") as f:
            data = json.load(f)

        if "associated_tools" not in data:
            data["associated_tools"] = []

        if tool_name in data["associated_tools"]:
            print(
                f"Info: Tool '{tool_name}' already exists in protocol '{protocol_id}'. No changes made."
            )
            return

        data["associated_tools"].append(tool_name)

        with open(protocol_file, "w") as f:
            json.dump(data, f, indent=2)

        print(
            f"Successfully added tool '{tool_name}' to protocol '{protocol_id}' in file '{protocol_file}'."
        )

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error processing protocol file '{protocol_file}': {e}")
        exit(1)


def update_rule_in_protocol(
    protocol_id: str, rule_id: str, new_description: str, protocols_dir: str
):
    """
    Updates the description of a specific rule within a protocol.
    """
    protocol_file = find_protocol_file(protocol_id, protocols_dir)
    if not protocol_file:
        print(
            f"Error: Protocol with ID '{protocol_id}' not found in '{protocols_dir}'."
        )
        exit(1)

    try:
        with open(protocol_file, "r") as f:
            data = json.load(f)

        if "rules" not in data or not isinstance(data["rules"], list):
            print(
                f"Error: Protocol '{protocol_id}' does not contain a valid 'rules' list."
            )
            exit(1)

        rule_found = False
        for rule in data["rules"]:
            if rule.get("rule_id") == rule_id:
                rule["description"] = new_description
                rule_found = True
                break

        if not rule_found:
            print(
                f"Error: Rule with ID '{rule_id}' not found in protocol '{protocol_id}'."
            )
            exit(1)

        with open(protocol_file, "w") as f:
            json.dump(data, f, indent=2)

        print(
            f"Successfully updated rule '{rule_id}' in protocol '{protocol_id}' with new description."
        )

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error processing protocol file '{protocol_file}': {e}")
        exit(1)


def main():
    """Main function to parse arguments and call the appropriate handler."""
    parser = argparse.ArgumentParser(
        description="Programmatically update protocol source files."
    )
    parser.add_argument(
        "--protocols-dir",
        default=DEFAULT_PROTOCOLS_DIR,
        help="The directory containing the protocol source files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 'add-tool' command ---
    parser_add_tool = subparsers.add_parser(
        "add-tool", help="Add a tool to a protocol."
    )
    parser_add_tool.add_argument(
        "--protocol-id", required=True, help="The ID of the protocol to modify."
    )
    parser_add_tool.add_argument(
        "--tool-name", required=True, help="The name of the tool to add."
    )

    # --- 'update-rule' command ---
    parser_update_rule = subparsers.add_parser(
        "update-rule", help="Update a rule's description in a protocol."
    )
    parser_update_rule.add_argument(
        "--protocol-id", required=True, help="The ID of the protocol to modify."
    )
    parser_update_rule.add_argument(
        "--rule-id", required=True, help="The ID of the rule to update."
    )
    parser_update_rule.add_argument(
        "--description", required=True, help="The new description for the rule."
    )

    args = parser.parse_args()

    if args.command == "add-tool":
        add_tool_to_protocol(args.protocol_id, args.tool_name, args.protocols_dir)
    elif args.command == "update-rule":
        update_rule_in_protocol(
            args.protocol_id, args.rule_id, args.description, args.protocols_dir
        )


if __name__ == "__main__":
    main()
