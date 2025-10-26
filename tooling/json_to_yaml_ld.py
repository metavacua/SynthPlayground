import json
import yaml
import sys

def convert_json_to_yaml_ld(filepath):
    """Converts a JSON file to YAML-LD."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Convert the JSON data to YAML
    print(yaml.dump(data, default_flow_style=False))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python json_to_yaml_ld.py <filepath>")
        sys.exit(1)
    convert_json_to_yaml_ld(sys.argv[1])
