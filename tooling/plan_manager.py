"""
Provides a command-line interface for managing the agent's Plan Registry.

This script is the administrative tool for the Plan Registry, a key component
of the Context-Free Development Cycle (CFDC) that enables hierarchical and
modular planning. The registry, located at `knowledge_core/plan_registry.json`,
maps human-readable, logical names to the file paths of specific plans. This
decouples the `call_plan` directive from hardcoded file paths, making plans
more reusable and the system more robust.

This CLI provides three essential functions:
- **register**: Associates a new logical name with a plan file path, adding it
  to the central registry.
- **deregister**: Removes an existing logical name and its associated path from
  the registry.
- **list**: Displays all current name-to-path mappings in the registry.

By providing a simple, standardized interface for managing this library of
reusable plans, this tool improves the agent's ability to compose complex
workflows from smaller, validated sub-plans.
"""

import argparse
import json
import os
import sys

REGISTRY_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "knowledge_core", "plan_registry.json"
    )
)


def get_registry():
    """Loads the plan registry from its JSON file."""
    if not os.path.exists(REGISTRY_PATH):
        return {}
    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(
            f"Warning: Could not read or parse registry at {REGISTRY_PATH}",
            file=sys.stderr,
        )
        return {}


def save_registry(registry_data):
    """Saves the given data to the plan registry JSON file."""
    try:
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry_data, f, indent=2)
        return True
    except IOError:
        print(f"Error: Could not write to registry at {REGISTRY_PATH}", file=sys.stderr)
        return False


def register_plan(name, path):
    """Registers a new plan by mapping a logical name to a file path."""
    if not os.path.exists(path):
        print(f"Error: The specified plan file does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    registry = get_registry()
    if name in registry:
        print(
            f"Error: The logical name '{name}' is already registered.",
            file=sys.stderr,
        )
        print(f"  Current path: {registry[name]}", file=sys.stderr)
        print(
            "  Use a different name or deregister the existing one first.",
            file=sys.stderr,
        )
        sys.exit(1)

    registry[name] = path
    if save_registry(registry):
        print(f"Successfully registered '{name}' -> '{path}'")


def deregister_plan(name):
    """Removes a plan from the registry by its logical name."""
    registry = get_registry()
    if name not in registry:
        print(
            f"Error: Logical name '{name}' not found in the registry.", file=sys.stderr
        )
        sys.exit(1)

    del registry[name]
    if save_registry(registry):
        print(f"Successfully deregistered '{name}'.")


def list_plans():
    """Lists all currently registered plans."""
    registry = get_registry()
    if not registry:
        print("The plan registry is currently empty.")
        return

    print("--- Registered Plans ---")
    max_len = max(len(name) for name in registry.keys()) if registry else 0
    for name, path in sorted(registry.items()):
        print(f"{name.ljust(max_len)} : {path}")
    print("------------------------")


def main():
    """Main function to run the plan management CLI."""
    parser = argparse.ArgumentParser(description="A tool to manage the Plan Registry.")
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    register_parser = subparsers.add_parser(
        "register", help="Register a new plan with a logical name."
    )
    register_parser.add_argument("name", help="The logical name for the plan.")
    register_parser.add_argument("path", help="The file path to the plan.")

    deregister_parser = subparsers.add_parser(
        "deregister", help="Deregister a plan by its logical name."
    )
    deregister_parser.add_argument(
        "name", help="The logical name of the plan to remove."
    )

    subparsers.add_parser("list", help="List all registered plans.")

    args = parser.parse_args()
    if args.command == "register":
        register_plan(args.name, args.path)
    elif args.command == "deregister":
        deregister_plan(args.name)
    elif args.command == "list":
        list_plans()


if __name__ == "__main__":
    main()
