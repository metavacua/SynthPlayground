
import os
import sys
import json
from tooling.build_utils import find_files, load_schema, execute_code
from tooling.compile_protocols_logic import generate_agents_md_content

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
PROTOCOLS_DIR = os.path.join(ROOT_DIR, "protocols")
SCHEMA_FILE = os.path.join(PROTOCOLS_DIR, "protocol.schema.json")


def compile_module(module_dir):
    """Compiles the protocol files in a directory into a single AGENTS.md."""
    module_name = os.path.basename(module_dir)
    target_file = os.path.join(module_dir, "AGENTS.md")
    print(f"--- Starting Protocol Compilation for {module_name} Module ---")
    print(f"Source directory: {module_dir}")
    print(f"Target file: {target_file}")

    schema = load_schema(SCHEMA_FILE)
    if not schema:
        return

    all_md_files = sorted([os.path.join(module_dir, f) for f in find_files(".protocol.md", base_dir=module_dir, recursive=False)])
    all_json_files = sorted([os.path.join(module_dir, f) for f in find_files(".protocol.json", base_dir=module_dir, recursive=False)])

    md_files_content = []
    for file_path in all_md_files:
        with open(file_path, "r") as f:
            md_files_content.append(f.read())

    json_files_content = []
    for file_path in all_json_files:
        try:
            with open(file_path, "r") as f:
                protocol_data = json.load(f)
                for rule in protocol_data.get("rules", []):
                    if "executable_code" in rule:
                        execute_code(rule["executable_code"], protocol_data["protocol_id"], rule["rule_id"])
                json_files_content.append(protocol_data)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {file_path}", file=sys.stderr)

    final_output_string = generate_agents_md_content(module_name, md_files_content, json_files_content, schema)
    temp_target_file = target_file + ".tmp"
    with open(temp_target_file, "w") as f:
        f.write(final_output_string)
    os.rename(temp_target_file, target_file)
    print(f"Successfully compiled AGENTS.md for {module_name} module at {target_file}")

def main():
    """Main function to find and compile all protocol modules."""
    for root, dirs, files in os.walk(PROTOCOLS_DIR):
        if "module.json" in files:
            compile_module(root)

if __name__ == "__main__":
    main()
