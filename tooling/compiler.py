import json
import os
import glob
from typing import List, Dict, Any
import jsonschema

# Define the path to the protocol schema
SCHEMA_PATH = os.path.join("protocols", "protocol.schema.json")

def load_json_file(filepath: str) -> Any:
    """Loads a JSON file and returns its content."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading or parsing {filepath}: {e}")
        return None

def validate_protocol(protocol_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validates a protocol object against the JSON schema using the jsonschema library.
    """
    try:
        jsonschema.validate(instance=protocol_data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"Schema validation failed for {protocol_data.get('protocol_id', 'N/A')}: {e.message}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during validation for {protocol_data.get('protocol_id', 'N/A')}: {e}")
        return False

def find_protocol_files(search_path: str) -> List[str]:
    """Finds all '.protocol.json' files in the specified directory."""
    return glob.glob(os.path.join(search_path, '*.protocol.json'))

def format_protocol_as_markdown(protocol: Dict[str, Any]) -> str:
    """Formats a single protocol into a Markdown string."""
    md = []
    md.append(f"## Protocol: {protocol['protocol_id']}")
    md.append(f"_{protocol['description']}_")
    md.append("\n### Rules")
    for rule in protocol.get('rules', []):
        md.append(f"- **{rule['rule_id']}**: {rule['description']}")
        if 'enforcement' in rule:
            md.append(f"  - *Enforcement: {rule['enforcement']}*")
    if protocol.get('associated_tools'):
        md.append("\n### Associated Tools")
        for tool in protocol['associated_tools']:
            md.append(f"- `{tool}`")
    return "\n".join(md)

def compile_protocols(search_path: str, output_path: str):
    """
    Compiles all protocols in a directory into a single AGENTS.md file.
    """
    print(f"Starting compilation for protocols in: {search_path}")
    schema = load_json_file(SCHEMA_PATH)
    if not schema:
        print("Could not load protocol schema. Aborting.")
        return

    protocol_files = find_protocol_files(search_path)
    if not protocol_files:
        print(f"No protocol files found in {search_path}.")
        # If no protocols, create an empty or placeholder AGENTS.md
        with open(output_path, 'w') as f:
            f.write("# Agent Protocols\n\n*No protocols defined in this scope.*\n")
        return

    all_markdowns = ["# Agent Protocols\n"]
    all_markdowns.append("_This document is auto-generated from protocol source files. Do not edit it directly._\n")

    for proto_file in sorted(protocol_files):
        protocol_data = load_json_file(proto_file)
        if protocol_data and validate_protocol(protocol_data, schema):
            print(f"  - Compiling {proto_file}")
            all_markdowns.append(format_protocol_as_markdown(protocol_data))
            all_markdowns.append("\n---\n")

    with open(output_path, 'w') as f:
        f.write("\n".join(all_markdowns))
    print(f"Successfully compiled protocols to: {output_path}")

if __name__ == '__main__':
    # This allows the script to be run directly for testing.
    # By default, it compiles the root 'protocols' directory.
    compile_protocols('protocols', 'protocols/AGENTS.md')