"""
A tool for auditing the agent's Plan Registry to ensure its integrity.

This script is a diagnostic and maintenance tool designed to validate the
`knowledge_core/plan_registry.json` file. The Plan Registry is a critical
component of the hierarchical planning system (CFDC), as it maps logical plan
names to their physical file paths. If this registry contains "dead links"
(i.e., entries that point to files that have been moved, renamed, or deleted),
the agent's ability to execute complex, multi-stage plans will be compromised.

This auditor performs one key function:
- **Dead Link Detection:** It reads every entry in the plan registry and verifies
  that the file path associated with each logical name actually exists in the
  filesystem.

The script provides a clear, human-readable report of which registry entries are
valid and which are invalid. This allows for quick identification and correction
of issues, helping to maintain the health and reliability of the agent's core
planning capabilities. It can be run manually for diagnostics or integrated into
automated health checks.
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