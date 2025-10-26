import json
import sys
import yaml
from pathlib import Path

# --- Configuration ---
ROOT_DIR = Path(__file__).parent.parent.resolve()
CONTEXT_FILE = ROOT_DIR / "protocols" / "protocol.context.jsonld"


def main():
    """
    Converts a JSON protocol file to a YAML-LD file by prepending the standard context.

    Usage:
        python tooling/json_to_yaml_ld.py <input_json_file> <output_yaml_file>
    """
    if len(sys.argv) != 3:
        print(main.__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: Input file not found at {input_file}", file=sys.stderr)
        sys.exit(1)

    if not CONTEXT_FILE.exists():
        print(f"Error: Context file not found at {CONTEXT_FILE}", file=sys.stderr)
        sys.exit(1)

    # Load the standard context
    with open(CONTEXT_FILE, "r") as f:
        context_data = json.load(f)

    # Load the source JSON data
    with open(input_file, "r") as f:
        json_data = json.load(f)

    # Combine context and data into a new dictionary
    # The '@context' key must be first for readability.
    combined_data = {**context_data, **json_data}

    # Write the combined data to the output YAML file
    # Use sort_keys=False to preserve the order (especially '@context' at the top)
    try:
        with open(output_file, "w") as f:
            yaml.dump(combined_data, f, indent=2, sort_keys=False, default_flow_style=False)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error writing YAML file {output_file}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
