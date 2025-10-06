import os
import json
import glob

def find_package_json_files(root_dir):
    """Finds all package.json files in the repository, excluding node_modules."""
    all_files = glob.glob(os.path.join(root_dir, '**', 'package.json'), recursive=True)
    return [f for f in all_files if 'node_modules' not in f]

def parse_dependencies(package_json_path):
    """Parses a single package.json file to extract its name and dependencies."""
    try:
        with open(package_json_path, 'r') as f:
            data = json.load(f)

        package_name = data.get('name', os.path.basename(os.path.dirname(package_json_path)))
        dependencies = list(data.get('dependencies', {}).keys())
        dev_dependencies = list(data.get('devDependencies', {}).keys())

        return {
            "package_name": package_name,
            "path": package_json_path,
            "dependencies": dependencies,
            "dev_dependencies": dev_dependencies
        }
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not parse {package_json_path}. Error: {e}")
        return None

def generate_dependency_graph(root_dir='.'):
    """Generates a dependency graph for all package.json files found."""
    graph = {
        "nodes": [],
        "edges": []
    }

    package_files = find_package_json_files(root_dir)
    package_info_list = []

    for pf in package_files:
        info = parse_dependencies(pf)
        if info:
            package_info_list.append(info)
            graph["nodes"].append({
                "id": info["package_name"],
                "path": info["path"]
            })

    # Create edges
    package_names = {p["package_name"] for p in package_info_list}
    for package in package_info_list:
        all_deps = package["dependencies"] + package["dev_dependencies"]
        for dep in all_deps:
            if dep in package_names: # Only create edges for internal packages
                graph["edges"].append({
                    "source": package["package_name"],
                    "target": dep
                })

    return graph

def main():
    """Main function to generate and save the dependency graph."""
    print("Generating dependency graph...")
    graph = generate_dependency_graph()

    output_path = os.path.join('knowledge_core', 'dependency_graph.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(graph, f, indent=2)

    print(f"Dependency graph successfully generated at {output_path}")

if __name__ == '__main__':
    main()