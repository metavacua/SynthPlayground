import os
import subprocess
import json
import re

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOCOLS_DIR_NAME = "protocols"
AGENTS_MD_FILENAME = "AGENTS.md"
README_FILENAME = "README.md"
PROTOCOL_COMPILER_PATH = os.path.join(os.path.dirname(__file__), "protocol_compiler.py")
README_GENERATOR_PATH = os.path.join(os.path.dirname(__file__), "readme_generator.py")
SUMMARY_FILE_PREFIX = "_z_child_summary_"
SPECIAL_DIRS = ["protocols/security"] # Directories to be ignored by the hierarchical scan

def find_protocol_dirs(root_dir):
    """
    Finds all directories named 'protocols' within the root directory,
    ignoring any special-cased directories.
    """
    protocol_dirs = []
    special_paths = {os.path.join(root_dir, d) for d in SPECIAL_DIRS}

    for dirpath, dirnames, _ in os.walk(root_dir):
        if PROTOCOLS_DIR_NAME in dirnames:
            proto_dir_path = os.path.join(dirpath, PROTOCOLS_DIR_NAME)
            if proto_dir_path in special_paths:
                print(f"Ignoring special directory: {proto_dir_path}")
                continue
            protocol_dirs.append(proto_dir_path)

    # Process from the deepest directories upwards to ensure children are built before parents
    return sorted(protocol_dirs, key=lambda x: -x.count(os.sep))

def run_compiler(source_dir):
    """Invokes the protocol_compiler.py script as a subprocess."""
    parent_dir = os.path.dirname(source_dir)
    target_agents_md = os.path.join(parent_dir, AGENTS_MD_FILENAME)

    command = [
        "python3",
        PROTOCOL_COMPILER_PATH,
        "--source-dir", source_dir,
        "--output-file", target_agents_md,
        "--knowledge-graph-file", os.path.join(ROOT_DIR, "knowledge_core", "protocols.ttl")
    ]

    print(f"Running AGENTS.md compiler for: {source_dir}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully compiled {target_agents_md}")
        return target_agents_md
    except subprocess.CalledProcessError as e:
        print(f"Error compiling AGENTS.md in {source_dir}:")
        print(e.stderr)
        return None

def run_readme_generator(source_agents_md):
    """Invokes the readme_generator.py script as a subprocess."""
    parent_dir = os.path.dirname(source_agents_md)
    target_readme = os.path.join(parent_dir, README_FILENAME)

    command = [
        "python3",
        README_GENERATOR_PATH,
        "--source-file", source_agents_md,
        "--output-file", target_readme
    ]

    print(f"Running README.md generator for: {source_agents_md}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully generated {target_readme}")
        return target_readme
    except subprocess.CalledProcessError as e:
        print(f"Error generating README.md for {source_agents_md}:")
        print(e.stderr)
        return None

def generate_summary(child_module_path):
    """
    Generates a machine-readable, JSON-LD summary of a child module.
    """
    child_dir_name = os.path.basename(child_module_path)

    summary_data = {
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "agents": "https://www.jules-project.org/agents/ns#",
            "hasMember": "prov:hasMember"
        },
        "@id": f"agents:{child_dir_name}",
        "@type": "agents:Module",
        "hasMember": {
            "@id": f"agents:{child_dir_name}/AGENTS.md"
        }
    }

    summary_md = f"## Child Module: `{child_dir_name}`\n\n"
    summary_md += "This module is defined by the protocols in its corresponding `AGENTS.md` file.\n\n"
    summary_md += f"```json\n{json.dumps(summary_data, indent=2)}\n```\n\n"
    summary_md += "---\n"

    return summary_md

def cleanup_summaries(directory):
    """Removes temporary summary files from a protocols directory."""
    if not os.path.isdir(directory):
        return
    for filename in os.listdir(directory):
        if filename.startswith(SUMMARY_FILE_PREFIX):
            os.remove(os.path.join(directory, filename))
            print(f"Cleaned up summary file: {filename}")

def get_parent_module(module_path, all_module_paths):
    """Finds the direct parent module of a given module."""
    parent_path = os.path.dirname(module_path)
    while len(parent_path) >= len(ROOT_DIR) and parent_path != "/":
        if parent_path in all_module_paths:
            return parent_path
        parent_path = os.path.dirname(parent_path)
    return None

def main():
    """
    Main function to orchestrate the hierarchical compilation.
    """
    print("--- Starting Hierarchical Build ---")
    all_protocol_dirs = find_protocol_dirs(ROOT_DIR)
    module_paths = [os.path.dirname(p) for p in all_protocol_dirs]

    compiled_artifacts = {}

    for proto_dir in all_protocol_dirs:
        current_module_path = os.path.dirname(proto_dir)
        print(f"\n--- Processing Module: {current_module_path} ---")

        # Inject summaries from children that have already been compiled
        for child_module_path, artifacts in compiled_artifacts.items():
            parent_module = get_parent_module(child_module_path, module_paths)
            if parent_module == current_module_path:
                print(f"Found compiled child: {child_module_path}. Generating summary.")
                summary_content = generate_summary(child_module_path)
                if summary_content:
                    summary_filename = f"{SUMMARY_FILE_PREFIX}{os.path.basename(child_module_path)}.protocol.md"
                    summary_filepath = os.path.join(proto_dir, summary_filename)
                    with open(summary_filepath, 'w') as f:
                        f.write(summary_content)
                    print(f"Injected summary for '{child_module_path}' into {summary_filepath}")

        # Compile the current module's AGENTS.md
        target_agents_md = run_compiler(proto_dir)
        if target_agents_md:
            # Generate the corresponding README.md
            target_readme = run_readme_generator(target_agents_md)
            compiled_artifacts[current_module_path] = {
                "agents_md": target_agents_md,
                "readme": target_readme
            }

        # Clean up the temporary summary files
        cleanup_summaries(proto_dir)

    print("\n--- Hierarchical Build Summary ---")
    for module, artifacts in sorted(compiled_artifacts.items()):
        print(f"Module: {module}")
        if artifacts.get('agents_md'):
            print(f"  - Compiled: {artifacts['agents_md']}")
        if artifacts.get('readme'):
            print(f"  - Generated: {artifacts['readme']}")


    print("\n--- Hierarchical Build Finished ---")

if __name__ == "__main__":
    main()