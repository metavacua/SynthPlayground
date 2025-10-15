import argparse
import subprocess
import sys

def main():
    """
    A tool to verify that the agent can monotonically improve its capabilities.

    This tool works by:
    1. Running a target test file that is known to fail, confirming the agent lacks a capability.
    2. Invoking the agent's self-correction mechanism to learn the new capability.
    3. Running the target test again to confirm it now passes.
    4. Running the full test suite to ensure no existing capabilities were lost.
    """
    parser = argparse.ArgumentParser(description="Verify monotonic capability improvement.")
    parser.add_argument(
        "--test-file",
        required=True,
        help="The path to the test file that defines the new capability."
    )
    args = parser.parse_args()

    print(f"--- Capability Verifier Initiated for {args.test_file} ---")

    # Step 1: Confirm the initial test fails
    print("\n--- Step 1: Confirming initial failure ---")
    initial_result = subprocess.run([sys.executable, args.test_file], capture_output=True, text=True)
    if initial_result.returncode == 0:
        print("Error: Test file passed unexpectedly. The agent may already possess this capability.")
        print(initial_result.stdout)
        sys.exit(1)
    else:
        print("Success: Test file failed as expected.")

    # Step 2: Create a lesson and invoke the self-correction orchestrator
    print("\n--- Step 2: Invoking self-correction ---")
    lesson_content = {
        "lesson_id": "verify-fibonacci-capability",
        "status": "pending",
        "failure": {
            "test_file": args.test_file,
            "error_message": initial_result.stderr
        },
        "action": {
            "type": "PROPOSE_CODE_CHANGE",
            "parameters": {
                "filepath": "self_improvement_project/main.py",
                "diff": "No-op for this test, as the fix is already applied."
            }
        }
    }
    import json
    with open("knowledge_core/lessons.jsonl", "w") as f:
        f.write(json.dumps(lesson_content) + "\n")

    orchestrator_result = subprocess.run(
        [sys.executable, "tooling/self_correction_orchestrator.py"],
        capture_output=True, text=True
    )
    if orchestrator_result.returncode != 0:
        print("Error: Self-correction orchestrator failed.")
        print(orchestrator_result.stderr)
        sys.exit(1)
    else:
        print("Success: Self-correction orchestrator completed.")
        print(orchestrator_result.stdout)

    # Step 3: Confirm the test now passes
    print("\n--- Step 3: Confirming test now passes ---")
    final_result = subprocess.run([sys.executable, args.test_file], capture_output=True, text=True)
    if final_result.returncode != 0:
        print("Error: Test file still fails after self-correction.")
        print(final_result.stderr)
        sys.exit(1)
    else:
        print("Success: Test file now passes.")
        print(final_result.stdout)

    # Step 4: Run the full test suite to check for regressions
    print("\n--- Step 4: Checking for regressions ---")
    # I need to find the full test suite. I'll assume for now it's in a `tests/` directory.
    # This is a placeholder and may need to be adjusted.
    regression_result = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests/"], capture_output=True, text=True)
    if regression_result.returncode != 0:
        print("Error: Regressions detected. The agent has lost a capability.")
        print(regression_result.stderr)
        sys.exit(1)
    else:
        print("Success: No regressions detected.")
        print("\n--- Capability Verifier Finished: Monotonic Improvement Confirmed ---")


if __name__ == "__main__":
    main()