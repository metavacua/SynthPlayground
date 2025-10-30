
import argparse
import os
import yaml
import json

def main():
    """Integrates knowledge from various YAML-LD sources into a single JSON-LD file."""
    parser = argparse.ArgumentParser(
        description="Integrate knowledge from various YAML-LD sources."
    )
    parser.add_argument(
        "--source-file",
        action="append",
        dest="source_files",
        help="Source YAML-LD files to integrate.",
    )
    parser.add_argument("--output-file", required=True, help="Output JSON-LD file path.")
    args = parser.parse_args()

    # This will be the final JSON-LD structure
    integrated_json_ld = {
        "@context": "protocols/protocol.context.jsonld",
        "@graph": []
    }

    # Load, parse, and merge the @graph from each source file
    for source_file in args.source_files:
        if not os.path.exists(source_file):
            print(f"Warning: Source file not found: {source_file}")
            continue
        try:
            with open(source_file, 'r') as f:
                data = yaml.safe_load(f)
                if '@graph' in data and isinstance(data['@graph'], list):
                    integrated_json_ld['@graph'].extend(data['@graph'])
                elif 'protocol_id' in data:  # Handle single protocol files
                    integrated_json_ld['@graph'].append(data)
        except Exception as e:
            print(f"Error parsing {source_file}: {e}")
            continue

    # Write the merged JSON-LD to the output file
    with open(args.output_file, "w") as f:
        json.dump(integrated_json_ld, f, indent=2)

    print(f"Successfully integrated knowledge into {args.output_file}")

if __name__ == "__main__":
    main()
