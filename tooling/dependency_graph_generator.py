import json
import os
import re

# Define the paths for the input and output files
# This makes the script more maintainable.
REQUIREMENTS_FILE = "requirements.txt"
OUTPUT_DIR = "knowledge_core"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dependency_graph.json")

def generate_dependency_graph():
    """
    Parses the requirements.txt file to generate a simple JSON dependency graph.

    The graph represents each package as a node. For this initial version,
    it does not map relationships between packages, but simply lists them
    as dependencies of the root project.
    """
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"Error: '{REQUIREMENTS_FILE}' not found.")
        return

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dependencies = []
    try:
        with open(REQUIREMENTS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Use regex to strip version specifiers (e.g., ==, >=, <)
                    package_name = re.split(r'[=<>~]', line)[0].strip()
                    if package_name:
                        dependencies.append({
                            "id": package_name,
                            "type": "python-package",
                            "source": REQUIREMENTS_FILE
                        })
    except Exception as e:
        print(f"Error reading or parsing '{REQUIREMENTS_FILE}': {e}")
        return

    # Structure the final graph
    dependency_graph = {
        "project_name": "SynthPlayground",
        "nodes": [
            {"id": "root", "type": "project-root"}
        ] + dependencies,
        "edges": [
            {"from": "root", "to": dep["id"]} for dep in dependencies
        ]
    }

    # Write the JSON output to the file
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(dependency_graph, f, indent=4)
        print(f"Successfully generated dependency graph at '{OUTPUT_FILE}'")
    except Exception as e:
        print(f"Error writing to '{OUTPUT_FILE}': {e}")

if __name__ == "__main__":
    generate_dependency_graph()