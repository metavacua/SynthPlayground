"""
A command-line tool for managing agent protocols.

This script provides a set of commands for creating, testing, and versioning
agent protocols. It is designed to be used by developers to manage the
protocol lifecycle.
"""

import argparse
import os
import json


def create_protocol(name, directory):
    """
    Creates a new protocol from a template.
    """
    protocol_id = name.lower().replace(" ", "-")
    protocol_file_name = f"{protocol_id}.protocol.json"
    protocol_path = os.path.join(directory, protocol_file_name)

    if os.path.exists(protocol_path):
        print(f"Error: Protocol '{protocol_id}' already exists.")
        return

    protocol_data = {
        "protocol_id": protocol_id,
        "version": "1.0.0",
        "description": f"A protocol for {name}.",
        "rules": [],
        "associated_tools": [],
    }

    with open(protocol_path, "w") as f:
        json.dump(protocol_data, f, indent=2)

    print(f"Created protocol '{protocol_id}' at {protocol_path}")


def run_tests():
    """
    Runs the protocol tests.
    """
    os.system("python3 tests/protocols/test_runner.py")


def main():
    """
    Main function for the protocol manager.
    """
    parser = argparse.ArgumentParser(description="A tool for managing agent protocols.")
    subparsers = parser.add_subparsers(dest="command")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new protocol.")
    create_parser.add_argument("name", help="The name of the protocol.")
    create_parser.add_argument(
        "--dir", default="protocols", help="The directory to create the protocol in."
    )

    # Test command
    subparsers.add_parser("test", help="Run the protocol tests.")

    # Version command
    version_parser = subparsers.add_parser(
        "version", help="Update the version of a protocol."
    )
    version_parser.add_argument("protocol_id", help="The ID of the protocol to update.")
    version_parser.add_argument("version", help="The new version.")

    args = parser.parse_args()

    if args.command == "create":
        create_protocol(args.name, args.dir)
    elif args.command == "test":
        run_tests()
    elif args.command == "version":
        update_version(args.protocol_id, args.version)


def update_version(protocol_id, new_version):
    """
    Updates the version of a protocol.
    """
    for root, dirs, files in os.walk("protocols"):
        for file in files:
            if file == f"{protocol_id}.protocol.json":
                protocol_path = os.path.join(root, file)
                with open(protocol_path, "r") as f:
                    protocol_data = json.load(f)

                protocol_data["version"] = new_version

                with open(protocol_path, "w") as f:
                    json.dump(protocol_data, f, indent=2)

                print(f"Updated version of '{protocol_id}' to {new_version}")
                return

    print(f"Error: Protocol '{protocol_id}' not found.")


if __name__ == "__main__":
    main()
