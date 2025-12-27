#!/usr/bin/env python3
"""
Directory Mapper for AGENTS.md Generation

This script discovers all directories in the repository and determines
which should have AGENTS.md files based on the agents_md_mapping.yaml config.
"""

import os
import yaml
import sys


def discover_directories(project_root):
    """Discover all directories in the project."""
    directories = []

    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories and common exclusions
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and d not in ["__pycache__", "node_modules", "venv", "env"]
        ]

        rel_path = os.path.relpath(root, project_root)
        if rel_path == ".":
            rel_path = "/"
        else:
            rel_path = "/" + rel_path

        directories.append(rel_path)

    return sorted(directories)


def load_mapping_config(config_path):
    """Load the agents_md_mapping.yaml configuration."""
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        return {}


def should_generate_agents_md(directory, mapping_config):
    """Determine if an AGENTS.md should be generated for this directory."""
    # Explicitly listed directories should always get AGENTS.md
    if directory in mapping_config:
        return True

    # Default logic: generate for directories with Python files or significant content
    if directory == "/":
        return True

    # Check if directory has meaningful content
    dir_path = directory[1:] if directory != "/" else ""
    full_path = os.path.join(os.getcwd(), dir_path)

    if not os.path.exists(full_path):
        return False

    # Count relevant files
    relevant_files = []
    for item in os.listdir(full_path):
        item_path = os.path.join(full_path, item)
        if os.path.isfile(item_path):
            if item.endswith(
                (".py", ".md", ".yaml", ".json", ".js", ".ts", ".html", ".css")
            ):
                if not item.startswith("."):
                    relevant_files.append(item)

    # Generate AGENTS.md if directory has 3+ relevant files or is explicitly configured
    return len(relevant_files) >= 3


def get_directory_protocols(directory, mapping_config):
    """Get the protocols that should be included for this directory."""
    if directory in mapping_config:
        return mapping_config[directory].get("protocols", [])
    elif "__default__" in mapping_config:
        return mapping_config["__default__"].get("protocols", [])
    else:
        return ["BEST-PRACTICES-001", "NON-COMPLIANCE-PROTOCOL-001"]


def get_directory_description(directory, mapping_config):
    """Get the description for this directory."""
    if directory in mapping_config:
        return mapping_config[directory].get(
            "description", f"Protocols for {directory}"
        )
    elif "__default__" in mapping_config:
        return mapping_config["__default__"].get(
            "description", f"Default protocols for {directory}"
        )
    else:
        return f"Protocols for {directory}"


def main():
    """Main entry point."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "agents_md_mapping.yaml")

    # Load mapping configuration
    mapping_config = load_mapping_config(config_path)

    # Discover all directories
    directories = discover_directories(project_root)

    # Determine which directories need AGENTS.md
    agents_md_directories = []
    for directory in directories:
        if should_generate_agents_md(directory, mapping_config):
            protocols = get_directory_protocols(directory, mapping_config)
            description = get_directory_description(directory, mapping_config)
            agents_md_directories.append(
                {
                    "directory": directory,
                    "protocols": protocols,
                    "description": description,
                }
            )

    # Output as JSON for consumption by generator
    import json

    output = {
        "directories": agents_md_directories,
        "total_count": len(agents_md_directories),
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
