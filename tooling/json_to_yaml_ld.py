import json
import yaml
import sys
import os

def convert_json_to_yaml_ld(directory, context_filepath):
    """Converts all JSON files in a directory to YAML-LD."""
    with open(context_filepath, 'r') as f:
        context = json.load(f)

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)

                # Add the context to the data only if it's a dictionary
                if isinstance(data, dict):
                    data['@context'] = context['@context']

                # Convert the JSON data to YAML
                yaml_filepath = os.path.splitext(filepath)[0] + '.yaml'
                with open(yaml_filepath, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python json_to_yaml_ld.py <directory> <context_filepath>")
        sys.exit(1)
    convert_json_to_yaml_ld(sys.argv[1], sys.argv[2])
