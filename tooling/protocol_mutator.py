"""
A tool for programmatically mutating agent protocol files for experimentation.

This script allows for controlled modifications of protocol source files (`.protocol.json`).
It can be used to add, remove, or modify rules to test how changes in protocols
affect agent behavior.

Example Usage:
- Add a new rule:
  python tooling/protocol_mutator.py \
    --source protocols/some_protocol.protocol.json \
    --output experiments/some_protocol.variant.json \
    --mutation 'ADD_RULE:{"rule_id": "new-test-rule", "description": "A new rule for testing.", "enforcement": "Enforced by agent observation."}'

- Remove an existing rule:
  python tooling/protocol_mutator.py \
    --source protocols/some_protocol.protocol.json \
    --output experiments/some_protocol.variant.json \
    --mutation 'REMOVE_RULE:rule_to_be_removed'
"""

import json
import argparse
import os
import sys

def load_protocol(file_path):
    """Loads a protocol JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Source file not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        sys.exit(1)

def save_protocol(data, file_path):
    """Saves data to a JSON file."""
    # Ensure the output directory exists
    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved variant protocol to {file_path}")

def apply_mutation(protocol_data, mutation_str):
    """Applies a mutation to the protocol data."""
    try:
        mutation_type, mutation_content = mutation_str.split(':', 1)
        mutation_type = mutation_type.strip().upper()
        mutation_content = mutation_content.strip()

        if mutation_type == 'ADD_RULE':
            new_rule = json.loads(mutation_content)
            if 'rules' not in protocol_data:
                protocol_data['rules'] = []
            # Check for rule_id uniqueness
            if any(r['rule_id'] == new_rule.get('rule_id') for r in protocol_data['rules']):
                print(f"Error: Rule with ID '{new_rule.get('rule_id')}' already exists.")
                return None
            protocol_data['rules'].append(new_rule)
            print(f"Applied mutation: Added rule '{new_rule.get('rule_id')}'")
            return protocol_data

        elif mutation_type == 'REMOVE_RULE':
            rule_id_to_remove = mutation_content
            initial_rule_count = len(protocol_data.get('rules', []))
            protocol_data['rules'] = [r for r in protocol_data.get('rules', []) if r.get('rule_id') != rule_id_to_remove]
            if len(protocol_data.get('rules', [])) < initial_rule_count:
                print(f"Applied mutation: Removed rule '{rule_id_to_remove}'")
            else:
                print(f"Warning: Rule with ID '{rule_id_to_remove}' not found. No change made.")
            return protocol_data

        else:
            print(f"Error: Unknown mutation type '{mutation_type}'")
            return None

    except Exception as e:
        print(f"Error parsing or applying mutation: {e}")
        return None

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Mutates an agent protocol file.")
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source .protocol.json file."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the mutated .protocol.json file."
    )
    parser.add_argument(
        "--mutation",
        required=True,
        help="The mutation to apply, e.g., 'ADD_RULE:{\"rule_id\": ...}' or 'REMOVE_RULE:some-id'"
    )

    args = parser.parse_args()

    # Load
    protocol_data = load_protocol(args.source)

    # Mutate
    mutated_data = apply_mutation(protocol_data, args.mutation)

    # Save
    if mutated_data:
        save_protocol(mutated_data, args.output)
    else:
        print("Mutation failed. Aborting.")
        sys.exit(1)

if __name__ == "__main__":
    main()