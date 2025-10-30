import argparse
import glob
import os
import yaml

def compile_protocols(output_file):
    """
    Compiles all protocol source files in the 'protocols/' directory into a single
    YAML-LD file.
    """
    all_protocols = {"@graph": []}

    # Use glob to find all protocol YAML files
    protocol_files = glob.glob("protocols/**/*.protocol.yaml", recursive=True)

    for source_file in protocol_files:
        with open(source_file, "r") as f:
            try:
                protocol_data = yaml.safe_load(f)
                all_protocols["@graph"].append(protocol_data)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML from {source_file}: {e}", file=sys.stderr)

    # Add context from a file
    context_file = "protocols/protocol.context.jsonld"
    if os.path.exists(context_file):
        with open(context_file, "r") as f:
            # Here we assume the context is a JSON object, so we load it as such
            import json
            try:
                all_protocols["@context"] = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing context JSON from {context_file}: {e}", file=sys.stderr)


    with open(output_file, "w") as f:
        yaml.dump(all_protocols, f, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(
        description="Compile all protocol sources from .protocol.yaml files into a single YAML-LD file."
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="The path to the output YAML-LD file.",
    )
    args = parser.parse_args()
    compile_protocols(args.output_file)
    print(f"Successfully compiled protocols to {args.output_file}")

if __name__ == "__main__":
    main()
