import json
import sys
from pathlib import Path

import yaml_ld


def main():
    """
    Converts a YAML-LD file to a JSON-LD file.

    Usage:
        python yaml_ld_to_json_ld.py <input_file> <output_file>
    """
    if len(sys.argv) != 3:
        print(main.__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: Input file not found at {input_file}")
        sys.exit(1)

    # Load the YAML-LD file and convert it to JSON-LD
    json_ld_data = yaml_ld.load_document(input_file)

    # The `load_document` function returns a dictionary with the document
    # under the "document" key. We only want to write the document itself.
    document = json_ld_data['document']

    # Write the JSON-LD data to the output file
    with open(output_file, "w") as f:
        json.dump(document, f, indent=2)


if __name__ == "__main__":
    main()
