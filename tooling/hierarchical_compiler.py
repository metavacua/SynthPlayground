import os
import sys
import subprocess
import json
import yaml # New import for YAML processing
import re

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOCOLS_DIR_NAME = "protocols"
AGENTS_MD_FILENAME = "AGENTS.md"
README_FILENAME = "README.md"
PROTOCOL_COMPILER_PATH = os.path.join(os.path.dirname(__file__), "protocol_compiler.py")
README_GENERATOR_PATH = os.path.join(os.path.dirname(__file__), "readme_generator.py")
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

def run_local_build_script(module_path):
    """Executes the local build script for a module, if it exists."""
    build_script_path = os.path.join(module_path, "build.sh")
    if not os.path.exists(build_script_path):
        print(f"No build script found for {module_path}. Skipping build.")
        return True # Return success if no script exists

    print(f"--> Executing local build script for {module_path}")
    try:
        # We run the script from the module's directory
        result = subprocess.run(
            ["/bin/bash", "build.sh"],
            cwd=module_path,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"Successfully built module: {module_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!! Error building module {module_path}:")
        print(e.stderr)
        return False

def verify_and_get_succedent(agents_md_path):
    """
    Verifies that the witnesses in a module's succedent exist and returns the succedent.
    """
    if not agents_md_path or not os.path.exists(agents_md_path):
        return None

    print(f"Verifying witnesses in: {agents_md_path}")
    with open(agents_md_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
            succedent = data.get('sequent', {}).get('succedent', [])
            module_dir = os.path.dirname(agents_md_path)

            for item in succedent:
                witness_path = os.path.join(module_dir, item['witness'])
                if not os.path.exists(witness_path):
                    print(f"!!! Witness file not found: {witness_path}")
                    raise FileNotFoundError(f"Witness file not found: {witness_path}")
                print(f"  - Witness verified: {witness_path}")
            return succedent
        except (yaml.YAMLError, FileNotFoundError) as e:
            print(f"!!! Error processing {agents_md_path}: {e}")
            return None


def generate_sequent_agents_md(target_path, antecedent, local_protocol_dir):
    """
    Generates the new AGENTS.md file in the YAML-based sequent format.
    """
    succedent = []
    if os.path.isdir(local_protocol_dir):
        for filename in os.listdir(local_protocol_dir):
            if filename.endswith(".protocol.json"):
                protocol_path = os.path.join(local_protocol_dir, filename)
                with open(protocol_path, 'r') as f:
                    try:
                        protocol_data = json.load(f)
                        # Assume the protocol file directly defines a succedent entry
                        if "id" in protocol_data and "type" in protocol_data and "proposition" in protocol_data and "witness" in protocol_data:
                             succedent.append({
                                 "id": protocol_data["id"],
                                 "type": protocol_data["type"],
                                 "proposition": protocol_data["proposition"],
                                 "witness": protocol_data["witness"]
                             })
                    except json.JSONDecodeError:
                        print(f"Warning: Could not decode JSON from {protocol_path}")

    if not succedent:
        # Create a default placeholder if no protocols are found
        succedent.append({
            "id": f"{os.path.basename(os.path.dirname(target_path))}_artifact",
            "type": "Placeholder",
            "proposition": "This module has no defined succedent. It may be a container for other modules.",
            "witness": "artifact.placeholder"
        })


    sequent = {
        "specVersion": "proof-theoretic-build/v1.0",
        "sequent": {
            "antecedent": antecedent,
            "succedent": succedent
        }
    }

    with open(target_path, 'w') as f:
        yaml.dump(sequent, f, default_flow_style=False, sort_keys=False)

    print(f"Successfully generated sequent: {target_path}")
    return target_path


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

def get_parent_module(module_path, all_module_paths):
    """Finds the direct parent module of a given module."""
    parent_path = os.path.dirname(module_path)
    # Ensure we don't go above the root directory
    if not parent_path.startswith(ROOT_DIR):
        return None
    while len(parent_path) >= len(ROOT_DIR) and parent_path != "/":
        if parent_path in all_module_paths:
            return parent_path
        parent_path = os.path.dirname(parent_path)
    if parent_path == ROOT_DIR and parent_path in all_module_paths:
        return parent_path
    return None

# Import the new finalizer script
from tooling.knowledge_graph_finalizer import generate_knowledge_graph

def main():
    """
    Main function to orchestrate the hierarchical, proof-theoretic build.
    """
    print("--- Starting Proof-Theoretic Build ---")
    protocol_dirs = find_protocol_dirs(ROOT_DIR)
    all_module_paths = [os.path.dirname(p) for p in protocol_dirs]

    # Ensure root is always considered a module, and it's processed last.
    if ROOT_DIR not in all_module_paths:
        all_module_paths.append(ROOT_DIR)

    # The loop should iterate over module paths, not just protocol dirs,
    # and in a way that parents are processed after children.
    sorted_module_paths = sorted(all_module_paths, key=lambda x: -len(x.split(os.sep)))


    compiled_artifacts = {}
    build_successful = True

    for current_module_path in sorted_module_paths:
        proto_dir = os.path.join(current_module_path, PROTOCOLS_DIR_NAME)
        print(f"\n--- Processing Module: {current_module_path} ---")

        # 1. Gather and verify antecedents from children
        antecedent = []
        build_halted = False
        for child_module_path, artifacts in compiled_artifacts.items():
            parent_module = get_parent_module(child_module_path, all_module_paths)
            if parent_module == current_module_path:
                print(f"Found child: {child_module_path}. Verifying its succedent.")
                child_succedent = verify_and_get_succedent(artifacts.get('agents_md'))
                if child_succedent is None:
                    print(f"!!! Halting build: Verification failed for child {child_module_path}")
                    build_halted = True
                    break
                # Remap child succedent to parent antecedent
                for item in child_succedent:
                    item['source'] = os.path.relpath(child_module_path, current_module_path)
                antecedent.extend(child_succedent)

        if build_halted:
            build_successful = False
            break

        # 2. Generate the AGENTS.md sequent for the current module
        target_agents_md = os.path.join(current_module_path, AGENTS_MD_FILENAME)
        generate_sequent_agents_md(target_agents_md, antecedent, proto_dir)

        # 3. Run the local build script for the module
        if not run_local_build_script(current_module_path):
             print(f"!!! Halting build: Local build script failed for {current_module_path}")
             build_successful = False
             break

        # 4. Verify self (succedent) and generate README
        final_succedent = verify_and_get_succedent(target_agents_md)
        if final_succedent is None:
            print(f"!!! Halting build: Self-verification failed for {current_module_path}")
            build_successful = False
            break

        target_readme = run_readme_generator(target_agents_md)

        # 5. Store compiled artifacts for parent
        compiled_artifacts[current_module_path] = {
            "agents_md": target_agents_md,
            "readme": target_readme,
            "succedent": final_succedent
        }


    print("\n--- Build Summary ---")
    for module, artifacts in sorted(compiled_artifacts.items()):
        print(f"Module: {module}")
        if artifacts.get('agents_md'):
            print(f"  - Sequent: {artifacts['agents_md']}")
        if artifacts.get('readme'):
            print(f"  - Specification: {artifacts['readme']}")

    if build_successful:
        print("\n--- Finalizing Build: Generating Root Knowledge Graph ---")
        jsonld_manifest = generate_knowledge_graph(ROOT_DIR)
        root_agents_md_path = os.path.join(ROOT_DIR, AGENTS_MD_FILENAME)
        try:
            with open(root_agents_md_path, "w") as f:
                f.write(jsonld_manifest)
            print(f"Successfully wrote knowledge graph manifest to {root_agents_md_path}")
        except IOError as e:
            print(f"!!! Error writing root manifest: {e}")
            build_successful = False


    if build_successful:
        print("\n--- Proof-Theoretic Build Finished Successfully ---")
    else:
        print("\n--- Proof-Theoretic Build FAILED ---")


if __name__ == "__main__":
    main()