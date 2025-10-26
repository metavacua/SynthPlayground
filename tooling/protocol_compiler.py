
import argparse
import json
import os
import re
import jsonschema
from yaml_ld import to_yaml_ld

def extract_json_from_markdown(filepath):
    """Extracts a JSON block from a Markdown file."""
    with open(filepath, "r") as f:
        content = f.read()
    match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return None

def main():
    """Compiles protocol sources into a single YAML-LD file."""
    parser = argparse.ArgumentParser(description="Compile protocol sources.")
    parser.add_argument(
        "--source-file",
        action="append",
        dest="source_files",
        help="Source files to compile.",
    )
    parser.add_argument("--output-file", required=True, help="Output file path.")
    args = parser.parse_args()

    # Load the JSON schema
    with open("protocols/protocol.schema.json", "r") as f:
        schema = json.load(f)

    # Compile all valid protocols into a single list
    compiled_protocols = []
    for source_file in args.source_files:
        if source_file.endswith(".md"):
            protocol_data = extract_json_from_markdown(source_file)
            if protocol_data:
                try:
                    jsonschema.validate(instance=protocol_data, schema=schema)
                    compiled_protocols.append(protocol_data)
                except jsonschema.exceptions.ValidationError as e:
                    print(f"Validation error in {source_file}: {e.message}")
                    continue

    # Create the JSON-LD structure
    json_ld_data = {
        "@context": "protocol.context.jsonld",
        "@graph": compiled_protocols,
    }

    # Convert JSON-LD to YAML-LD and write to the output file
    to_yaml_ld(json_ld_data, args.output_file)

    print(f"Successfully compiled protocols to {args.output_file}")

if __name__ == "__main__":
    main()
