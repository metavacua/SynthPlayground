import yaml
import argparse
import os
import json

def run_test(test_file, tool_name, args_json):
    """Parses a decision-making test file and interactively tests the agent's decision."""
    with open(test_file, 'r') as f:
        tests = yaml.safe_load(f)

    for test in tests:
        print(f"--- Running Test: {test['id']} ---")
        print(f"Scenario: {test['scenario']}\\n")

        print("--- Context ---")
        for i, item in enumerate(test['context']):
            print(f"Context Item {i+1}:")
            if item['type'] == 'file':
                print(f"  Type: File")
                print(f"  Path: {item['path']}")
                print(f"  Content:\\n{item['content']}")
            elif item['type'] == 'command_output':
                print(f"  Type: Command Output")
                print(f"  Command: {item['command']}")
                print(f"  Output:\\n{item['output']}")
            print("")

        try:
            args = json.loads(args_json)
        except json.JSONDecodeError:
            print("Error: Invalid JSON string for arguments.")
            print(f"--- Test {test['id']} Failed ---")
            continue

        expected_action = test['expected_action']
        if tool_name == expected_action['tool'] and args == expected_action['args']:
            print(f"\\n--- Test {test['id']} Passed ---")
        else:
            print(f"\\n--- Test {test['id']} Failed ---")
            print("Expected Action:")
            print(f"  Tool: {expected_action['tool']}")
            print(f"  Args: {expected_action['args']}")
            print("Your Action:")
            print(f"  Tool: {tool_name}")
            print(f"  Args: {args}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decision-Making Test Runner")
    parser.add_argument("test_file", help="The path to the decision-making test file.")
    parser.add_argument("tool_name", help="The name of the tool to be called.")
    parser.add_argument("args_json", help="The arguments as a JSON string.")
    args = parser.parse_args()

    if not os.path.exists(args.test_file):
        print(f"Error: Test file not found at {args.test_file}")
        exit(1)

    run_test(args.test_file, args.tool_name, args.args_json)
