import os
import json
import re


def parse_package_json_content(content, path):
    """
    Parses the content of a package.json file to extract its name and dependencies.
    """
    try:
        data = json.loads(content)
        package_name = data.get("name", os.path.basename(os.path.dirname(path)))
        dependencies = list(data.get("dependencies", {}).keys())
        dev_dependencies = list(data.get("devDependencies", {}).keys())

        return {
            "project_name": package_name,
            "path": path,
            "dependencies": dependencies + dev_dependencies,
            "type": "javascript",
        }
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse content from {path}. Error: {e}")
        return None


def parse_requirements_txt_content(content, path, root_dir):
    """
    Parses the content of a requirements.txt file to extract its dependencies.
    """
    lines = content.splitlines()
    dependencies = []
    for line in lines:
        # Strip comments and whitespace
        line = line.split("#")[0].strip()
        if line:
            # Use regex to get just the package name, ignoring version, extras, etc.
            match = re.match(r"^[a-zA-Z0-9_.-]+", line)
            if match:
                dependencies.append(match.group(0))

    # If the file is at the root of the scan, give it a special name.
    # Otherwise, use its parent directory's name.
    dir_name = os.path.dirname(path)
    if os.path.abspath(dir_name) == os.path.abspath(root_dir):
        project_name = "root-python-project"
    else:
        project_name = os.path.basename(dir_name)

    return {
        "project_name": project_name,
        "path": path,
        "dependencies": dependencies,
        "type": "python",
    }


def generate_dependency_graph_from_projects(all_projects):
    """
    Generates a dependency graph from a list of projects.
    """
    graph = {"nodes": [], "edges": []}

    # Add all projects as nodes
    project_names = {p["project_name"] for p in all_projects}
    for proj in all_projects:
        graph["nodes"].append(
            {
                "id": proj["project_name"],
                "path": proj["path"],
                "type": f"{proj['type']}-project",
            }
        )

    # Add dependencies as nodes and create edges
    node_ids = {n["id"] for n in graph["nodes"]}

    for proj in all_projects:
        source_id = proj["project_name"]
        for dep in proj["dependencies"]:
            target_id = dep

            # If the dependency is another project in our repo, it's an internal edge
            if target_id in project_names:
                graph["edges"].append({"source": source_id, "target": target_id})
            # Otherwise, it's an external dependency
            else:
                # Add the external dependency as a node if it doesn't exist yet
                if target_id not in node_ids:
                    graph["nodes"].append(
                        {
                            "id": target_id,
                            "path": None,
                            "type": f"{proj['type']}-external",
                        }
                    )
                    node_ids.add(target_id)
                graph["edges"].append({"source": source_id, "target": target_id})

    return graph
