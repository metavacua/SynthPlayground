import os
import json
import argparse

class SimulatedAgent:
    """
    A simplified agent simulation to test the effect of AGENTS.md files.
    This class mimics the core logic of an agent checking protocols before acting.
    """
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.protocols = self._load_protocols()

    def _load_protocols(self):
        """
        Finds and parses the nearest AGENTS.md file in the working directory.
        Returns a structured representation of the rules found.
        """
        path = os.path.join(self.working_dir, 'AGENTS.md')
        if not os.path.exists(path):
            return {"rules": []}

        with open(path, 'r') as f:
            content = f.read()

        try:
            # Attempt to parse the file as structured JSON.
            data = json.loads(content)
            return data
        except json.JSONDecodeError:
            # If it's not JSON, treat it as a plain-text, non-machine-readable rule.
            # This simulates the outcome of an ambiguous protocol.
            return {"rules": [{"id": "plain_text_rule", "description": content, "effect": "unknown"}]}

    def is_action_forbidden(self, tool_name):
        """
        Checks if the loaded protocols explicitly forbid the use of a specific tool.
        """
        for rule in self.protocols.get("rules", []):
            if rule.get("effect") == "deny" and tool_name in rule.get("tool_name", []):
                return True, rule
        return False, None

    def perform_standard_task(self):
        """
        Represents the standardized task for all experiments: create a specific file.
        The agent first checks its protocols and then acts, simulating the
        decision-making process.
        """
        tool_to_use = "create_file_with_block"

        is_forbidden, rule = self.is_action_forbidden(tool_to_use)

        if is_forbidden:
            return {
                "outcome": "BLOCKED",
                "reason": f"Action forbidden by machine-readable protocol rule: {rule.get('id')}",
                "rule": rule
            }

        # If not explicitly blocked by a 'deny' rule, the agent proceeds.
        try:
            # Clean up previous run's output if it exists
            output_path = os.path.join(self.working_dir, 'output.txt')
            if os.path.exists(output_path):
                os.remove(output_path)

            with open(output_path, 'w') as f:
                f.write('hello world')

            # Verify the action was successful
            with open(output_path, 'r') as f:
                content = f.read()
            if content == 'hello world':
                 return {"outcome": "SUCCESS", "details": "File 'output.txt' created successfully."}
            else:
                 return {"outcome": "FAILURE", "reason": "File content mismatch after writing."}

        except Exception as e:
            return {"outcome": "FAILURE", "reason": str(e)}


def main():
    """
    Main entry point for the experiment runner script.
    """
    parser = argparse.ArgumentParser(description="Run a standardized agent experiment.")
    parser.add_argument(
        '--directory',
        required=True,
        help="The path to the experiment directory to run."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found at {args.directory}")
        exit(1)

    # The agent's context is the specified directory.
    agent = SimulatedAgent(args.directory)

    # The agent attempts the standardized task.
    result = agent.perform_standard_task()

    # The outcome is recorded for later analysis.
    result_path = os.path.join(args.directory, 'results.json')
    with open(result_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Experiment finished for '{args.directory}'. Result: {result['outcome']}")
    print(f"Results saved to '{result_path}'")


if __name__ == "__main__":
    main()