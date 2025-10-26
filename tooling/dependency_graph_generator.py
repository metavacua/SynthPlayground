"""
Scans the repository for dependency files and generates a unified dependency graph.

This script is a crucial component of the agent's environmental awareness,
providing a clear map of the software supply chain. It recursively searches the
entire repository for common dependency management files, specifically:
- `package.json` (for JavaScript/Node.js projects)
- `requirements.txt` (for Python projects)

It parses these files to identify two key types of relationships:
1.  **Internal Dependencies:** Links between different projects within this repository.
2.  **External Dependencies:** Links to third-party libraries and packages.

The final output is a JSON file, `knowledge_core/dependency_graph.json`, which
represents these relationships as a graph structure with nodes (projects and
dependencies) and edges (the dependency links). This artifact is a primary
input for the agent's orientation and planning phases, allowing it to reason
about the potential impact of its changes.
"""

import argparse
import os
import json
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tooling.filesystem_lister import list_all_files_and_dirs
from tooling.dependency_graph_generator_logic import (
    parse_package_json_content,
    parse_requirements_txt_content,
    generate_dependency_graph_from_projects,
)


def find_dependency_files(root_dir):
    """Finds all package.json and requirements.txt files, excluding node_modules."""
    all_files = list_all_files_and_dirs(root_dir)
    package_json_files = [f for f in all_files if f.endswith("package.json")]
    requirements_txt_files = [f for f in all_files if f.endswith("requirements.txt")]
    return package_json_files, requirements_txt_files


def generate_dependency_graph(root_dir="."):
    """Generates a dependency graph for all supported dependency files found."""
    all_projects = []

    # Consolidate all discovered projects
    package_json_files, requirements_txt_files = find_dependency_files(root_dir)

    for pf_rel in package_json_files:
        pf_abs = os.path.join(root_dir, pf_rel)
        with open(pf_abs, "r") as f:
            content = f.read()
        info = parse_package_json_content(content, pf_abs)
        if info:
            all_projects.append(info)

    for rf_rel in requirements_txt_files:
        rf_abs = os.path.join(root_dir, rf_rel)
        with open(rf_abs, "r") as f:
            content = f.read()
        info = parse_requirements_txt_content(content, rf_abs, root_dir)
        if info:
            all_projects.append(info)

    return generate_dependency_graph_from_projects(all_projects)


def main():
    """Main function to generate and save the dependency graph."""
    parser = argparse.ArgumentParser(
        description="Generates a dependency graph for the repository."
    )
    parser.add_argument(
        "--output",
        default="knowledge_core/dependency_graph.json",
        help="The path to the output JSON file.",
    )
    args = parser.parse_args()

    print("Generating dependency graph...")
    graph = generate_dependency_graph()

    output_path = args.output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(graph, f, indent=2)

    print(f"Dependency graph successfully generated at {output_path}")


if __name__ == "__main__":
    main()
