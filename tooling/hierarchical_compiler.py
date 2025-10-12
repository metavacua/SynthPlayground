import os
import subprocess
import json
import re
import glob

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOCOLS_DIR_NAME = "protocols"
AGENTS_MD_FILENAME = "AGENTS.md"
README_FILENAME = "README.md"
PROTOCOL_COMPILER_PATH = os.path.join(os.path.dirname(__file__), "protocol_compiler.py")
README_GENERATOR_PATH = os.path.join(os.path.dirname(__file__), "readme_generator.py")
SUMMARY_FILE_PREFIX = "_z_child_summary_"
SPECIAL_DIRS = ["protocols/security", "examples"] # Directories to be ignored by the hierarchical scan

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

def run_compiler(source_dir, inherited_rules=None):
    """
    Invokes the protocol_compiler.py script as a subprocess, optionally passing
    a list of inherited rules.
    """
    parent_dir = os.path.dirname(source_dir)
    target_agents_md = os.path.join(parent_dir, AGENTS_MD_FILENAME)

    command = [
        "python3",
        PROTOCOL_COMPILER_PATH,
        "--source-dir", source_dir,
        "--output-file", target_agents_md,
        "--knowledge-graph-file"
    ]

    if inherited_rules:
        command.extend(["--inherited-rules", json.dumps(inherited_rules)])

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

def generate_summary(child_agents_md_path):
    """
    Generates a summary of a child AGENTS.md file by extracting protocol IDs.
    """
    if not child_agents_md_path or not os.path.exists(child_agents_md_path):
        return ""

    with open(child_agents_md_path, 'r') as f:
        content = f.read()

    json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)

    summaries = []
    for block in json_blocks:
        try:
            protocol_data = json.loads(block)
            protocol_id = protocol_data.get("protocol_id")
            if protocol_id:
                summaries.append(f"- `{protocol_id}`")
        except json.JSONDecodeError:
            continue

    if not summaries:
        return ""

    child_dir_name = os.path.basename(os.path.dirname(child_agents_md_path))
    summary_md = f"## Child Module: `{child_dir_name}`\n\n"
    summary_md += "This module contains the following protocols, which are defined in its own `AGENTS.md` file:\n\n"
    summary_md += "\n".join(sorted(summaries))
    summary_md += "\n\n---\n"

    return summary_md

def cleanup_summaries(directory):
    """Removes temporary summary files from a protocols directory."""
    if not os.path.isdir(directory):
        return
    for filename in os.listdir(directory):
        if filename.startswith(SUMMARY_FILE_PREFIX):
            os.remove(os.path.join(directory, filename))
            print(f"Cleaned up summary file: {filename}")

def find_all_protocol_source_files(directory):
    """Finds all .protocol.json files in a directory."""
    return glob.glob(os.path.join(directory, "*.protocol.json"))

def build_inheritance_map(all_protocol_dirs, module_paths, root_dir):
    """
    Walks the module tree from top to bottom to build a map of what rules
    each module inherits from its parents.
    """
    inheritance_map = {path: [] for path in module_paths}

    # Sort modules from top-level to deepest
    sorted_modules = sorted(module_paths, key=lambda x: x.count(os.sep))

    for module_path in sorted_modules:
        parent_module = get_parent_module(module_path, module_paths, root_dir)
        if parent_module:
            # Inherit rules from the direct parent
            inheritance_map[module_path].extend(inheritance_map[parent_module])

        # Add own inheritable rules to the map for children to inherit
        current_protocols_dir = os.path.join(module_path, PROTOCOLS_DIR_NAME)
        source_files = find_all_protocol_source_files(current_protocols_dir)

        for fpath in source_files:
            try:
                with open(fpath, 'r') as f:
                    data = json.load(f)

                inheritable_rules_def = data.get("inheritable_rules", [])
                if not inheritable_rules_def:
                    continue

                # Get the full rule object from the 'rules' list
                all_rules = {rule['rule_id']: rule for rule in data.get('rules', [])}
                for inheritable in inheritable_rules_def:
                    rule_id = inheritable.get("rule_id")
                    if rule_id in all_rules:
                        # Append the full rule object to the map
                        inheritance_map[module_path].append(all_rules[rule_id])

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not parse inheritable rules from {fpath}: {e}")
                continue

    return inheritance_map

def get_parent_module(module_path, all_module_paths, root_dir):
    """Finds the direct parent module of a given module."""
    parent_path = os.path.dirname(module_path)
    while len(parent_path) >= len(root_dir) and parent_path != "/":
        if parent_path in all_module_paths:
            return parent_path
        parent_path = os.path.dirname(parent_path)
    return None

def main(root_dir=None):
    """
    Main function to orchestrate the hierarchical compilation.
    If root_dir is None, it defaults to the repository's root.
    """
    if root_dir is None:
        root_dir = ROOT_DIR

    print("--- Starting Hierarchical Build ---")
    all_protocol_dirs = find_protocol_dirs(root_dir)
    module_paths = [os.path.dirname(p) for p in all_protocol_dirs]

    # First pass: build the inheritance map from top to bottom
    inheritance_map = build_inheritance_map(all_protocol_dirs, module_paths, root_dir)

    compiled_artifacts = {}

    # Second pass: build the artifacts from bottom to top
    for proto_dir in all_protocol_dirs:
        current_module_path = os.path.dirname(proto_dir)
        print(f"\n--- Processing Module: {current_module_path} ---")

        # Inject summaries from children that have already been compiled
        for child_module_path, artifacts in compiled_artifacts.items():
            parent_module = get_parent_module(child_module_path, module_paths, root_dir)
            if parent_module == current_module_path:
                print(f"Found compiled child: {child_module_path}. Generating summary.")
                summary_content = generate_summary(artifacts['agents_md'])
                if summary_content:
                    summary_filename = f"{SUMMARY_FILE_PREFIX}{os.path.basename(child_module_path)}.protocol.md"
                    summary_filepath = os.path.join(proto_dir, summary_filename)
                    with open(summary_filepath, 'w') as f:
                        f.write(summary_content)
                    print(f"Injected summary for '{child_module_path}' into {summary_filepath}")

        # Compile the current module's AGENTS.md, passing in any inherited rules
        inherited_rules = inheritance_map.get(current_module_path, [])
        target_agents_md = run_compiler(proto_dir, inherited_rules)
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