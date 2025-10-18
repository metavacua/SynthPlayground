import json
import argparse
import os

def log_step(message):
    """Prints a formatted step message."""
    print(f"--- {message} ---")

def apply_json_mutation(file_path, rule_id, field_to_change, new_value):
    """
    Applies a targeted mutation to a specific rule within a .protocol.json file.

    Args:
        file_path (str): The path to the .protocol.json file.
        rule_id (str): The 'rule_id' of the rule to be modified.
        field_to_change (str): The name of the field to change within the rule.
        new_value (str): The new value to set for the field.
    """
    log_step(f"Applying mutation to {os.path.basename(file_path)}: Change rule '{rule_id}' -> set '{field_to_change}' to '{new_value}'")

    if not os.path.exists(file_path):
        print(f"ERROR: File not found at {file_path}")
        return False

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        rule_found = False
        if 'rules' in data and isinstance(data['rules'], list):
            for rule in data['rules']:
                if rule.get('rule_id') == rule_id:
                    rule[field_to_change] = new_value
                    rule_found = True
                    break

        if not rule_found:
            print(f"ERROR: Rule with rule_id '{rule_id}' not found in {file_path}")
            return False

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        print("Mutation applied successfully.")
        return True

    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: Failed to read or write JSON file at {file_path}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def main():
    """Main function to orchestrate the mutation process."""
    parser = argparse.ArgumentParser(description="Agent Smith: Protocol Mutator")
    parser.add_argument(
        "--file",
        required=True,
        help="The path of the .protocol.json file to mutate."
    )
    parser.add_argument(
        "--rule-id",
        required=True,
        help="The ID of the rule to mutate within the JSON file."
    )
    parser.add_argument(
        "--field",
        required=True,
        help="The field within the rule to change."
    )
    parser.add_argument(
        "--value",
        required=True,
        help="The new value for the specified field."
    )
    args = parser.parse_args()

    if not apply_json_mutation(args.file, args.rule_id, args.field, args.value):
        exit(1)

if __name__ == "__main__":
    main()