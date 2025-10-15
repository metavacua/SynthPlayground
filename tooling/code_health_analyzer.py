"""
A tool for analyzing the overall health of the codebase.

This module currently focuses on the integrity of the plan registry,
providing functionality to detect and generate plans to fix "dead links"
(registry entries that point to non-existent files).
"""
import json
import os

# The repository root is the parent directory of the 'tooling' directory
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLAN_REGISTRY_PATH = os.path.join(REPO_ROOT, "knowledge_core", "plan_registry.json")

def get_dead_links_and_content():
    """
    Audits the plan registry, returns a list of dead links and the original content.
    """
    dead_links = []
    original_content = ""
    if not os.path.exists(PLAN_REGISTRY_PATH):
        return dead_links, original_content

    with open(PLAN_REGISTRY_PATH, "r") as f:
        try:
            original_content = f.read()
            content_to_parse = original_content.strip()
            if not content_to_parse:
                return [], original_content
            registry = json.loads(content_to_parse)
        except (IOError, json.JSONDecodeError):
            return [], original_content

    for name, path in registry.items():
        # Paths in the registry are relative to the repository root
        abs_path = os.path.join(REPO_ROOT, path)
        if not os.path.exists(abs_path):
            dead_links.append(name)

    return dead_links, registry

def generate_plan_to_fix_dead_links(dead_links, current_registry):
    """
    Generates a plan using `overwrite_file_with_block` to fix dead links.
    """
    if not dead_links:
        return ""

    # Create the corrected registry by removing the dead links
    for link in dead_links:
        if link in current_registry:
            del current_registry[link]

    # Format the new content
    new_content = json.dumps(current_registry, indent=2)

    # Generate a plan to overwrite the file with the corrected content
    plan = f"""overwrite_file_with_block
{PLAN_REGISTRY_PATH}
{new_content}
"""
    return plan

def main():
    """
    Main entry point for the code health analyzer.
    Identifies dead links and prints a plan to fix them.
    """
    dead_links, current_registry = get_dead_links_and_content()
    plan = generate_plan_to_fix_dead_links(dead_links, current_registry)
    if plan:
        print(plan)

if __name__ == "__main__":
    main()