import json
import argparse
import sys
import os

def load_json_file(path):
    """Loads a JSON file and returns its content."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Source protocol file not found at '{path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{path}'", file=sys.stderr)
        sys.exit(1)

def parse_rule_json(rule_json_str):
    """Parses a JSON string into a Python dictionary."""
    try:
        return json.loads(rule_json_str)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON provided for the rule.", file=sys.stderr)
        print(f"Received: {rule_json_str}", file=sys.stderr)
        sys.exit(1)

def mutate_protocol(protocol_data, new_rule):
    """
    Adds or updates a rule in the protocol data.
    If a rule with the same 'rule_id' exists, it's replaced.
    Otherwise, the new rule is appended.
    """
    if 'rule_id' not in new_rule:
        print(f"Error: The provided rule JSON must contain a 'rule_id'.", file=sys.stderr)
        sys.exit(1)

    new_rule_id = new_rule['rule_id']
    rule_found = False

    for i, existing_rule in enumerate(protocol_data.get('rules', [])):
        if existing_rule.get('rule_id') == new_rule_id:
            protocol_data['rules'][i] = new_rule
            rule_found = True
            break

    if not rule_found:
        if 'rules' not in protocol_data:
            protocol_data['rules'] = []
        protocol_data['rules'].append(new_rule)

    return protocol_data

def write_json_file(path, data):
    """Writes data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to output file at '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to run the protocol mutator."""
    parser = argparse.ArgumentParser(description="A tool to programmatically add or update rules in a protocol JSON file.")
    parser.add_argument("source_protocol", help="Path to the source protocol .json file.")
    parser.add_argument("rule_json", help="A JSON string representing the rule to add or update.")
    parser.add_argument("output_path", help="Path to write the mutated protocol file.")

    args = parser.parse_args()

    # 1. Load the source protocol
    protocol_data = load_json_file(args.source_protocol)

    # 2. Parse the new rule
    new_rule = parse_rule_json(args.rule_json)

    # 3. Mutate the protocol data
    mutated_data = mutate_protocol(protocol_data, new_rule)

    # 4. Write the new protocol file
    write_json_file(args.output_path, mutated_data)

    print(f"Successfully mutated protocol and saved to '{args.output_path}'")

if __name__ == "__main__":
    main()