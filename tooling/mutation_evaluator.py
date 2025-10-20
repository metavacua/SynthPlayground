import argparse
import subprocess
import os

def evaluate_mutation(sandbox_path):
    """
    Evaluates a mutation by running the test suite in a sandboxed environment.
    """
    if not os.path.isdir(sandbox_path):
        print(f"Error: Sandbox path not found at {sandbox_path}")
        return

    print(f"--- Running Mutation Evaluation in {sandbox_path} ---")

    try:
        # For simplicity, this tool assumes a Makefile with a 'test' target.
        # A more robust implementation would inspect the sandbox for test scripts.
        result = subprocess.run(
            ["make", "test"],
            cwd=sandbox_path,
            capture_output=True,
            text=True,
            check=True
        )
        print("--- Test Suite Succeeded ---")
        print(result.stdout)
        print("--- Mutation Evaluation: PASSED ---")

    except FileNotFoundError:
        print("Error: 'make' command not found. Is Make installed and in the system's PATH?")
        print("--- Mutation Evaluation: FAILED ---")

    except subprocess.CalledProcessError as e:
        print("--- Test Suite Failed ---")
        print("Return Code:", e.returncode)
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        print("--- Mutation Evaluation: FAILED ---")


def main():
    parser = argparse.ArgumentParser(description='A simple mutation evaluation tool.')
    parser.add_argument('sandbox_path', type=str, help='The path to the sandbox environment to evaluate.')
    args = parser.parse_args()
    evaluate_mutation(args.sandbox_path)

if __name__ == "__main__":
    main()
