"""
A tool for auditing the plan registry.

This script reads the `plan_registry.json` file and verifies that every
registered plan name points to a file that actually exists in the filesystem.
It provides a clear report of any "dead links," helping to maintain the
integrity of the hierarchical planning system.
"""
import json
import os
import argparse

DEFAULT_PLAN_REGISTRY_PATH = "knowledge_core/plan_registry.json"


def audit_plan_registry(registry_path=DEFAULT_PLAN_REGISTRY_PATH):
    """
    Audits the plan registry to find registered plans that point to
    non-existent files.

    Args:
        registry_path (str): The path to the plan registry JSON file.

    Returns:
        list: A list of tuples, where each tuple contains the name and
              path of a dead link.
    """
    print(f"Auditing Plan Registry: {registry_path}")
    dead_links = []

    if not os.path.exists(registry_path):
        print(f"Error: Plan registry not found at '{registry_path}'")
        return []

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{registry_path}'")
        return []


    for name, path in registry.items():
        if not os.path.exists(path):
            dead_links.append((name, path))
            print(f"  [INVALID] '{name}' -> '{path}' (File not found)")
        else:
            print(f"  [OK]      '{name}' -> '{path}'")

    if not dead_links:
        print("\nAudit complete. All registered plans are valid.")
    else:
        print(f"\nAudit complete. Found {len(dead_links)} dead link(s).")

    return dead_links

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit the plan registry for dead links.")
    parser.add_argument(
        "--registry-path",
        default=DEFAULT_PLAN_REGISTRY_PATH,
        help=f"Path to the plan registry file (default: {DEFAULT_PLAN_REGISTRY_PATH})"
    )
    args = parser.parse_args()

    audit_plan_registry(registry_path=args.registry_path)