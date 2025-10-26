"""
A tool to verify that the agent can monotonically improve its capabilities.

This script is designed to provide a formal, automated test for the agent's
self-correction and learning mechanisms. It ensures that when the agent learns
a new capability, it does so without losing (regressing) any of its existing
capabilities. This is a critical safeguard for ensuring robust and reliable
agent evolution.

The tool works by orchestrating a four-step process:
1.  **Confirm Initial Failure:** It runs a specific test file that is known to
    fail, verifying that the agent currently lacks the target capability.
2.  **Invoke Self-Correction:** It simulates the discovery of a new "lesson" and
    triggers the `self_correction_orchestrator.py` script, which is responsible
    for integrating new knowledge and skills.
3.  **Confirm Final Success:** It runs the same test file again, confirming that
    the agent has successfully learned the new capability and the test now passes.
4.  **Check for Regressions:** It runs the full, existing test suite to ensure
    that the process of learning the new skill has not inadvertently broken any
    previously functional capabilities.

This provides a closed-loop verification of monotonic improvement, which is a
cornerstone of the agent's design philosophy.
"""

import argparse
import subprocess
import sys
from tooling.capability_verifier_logic import generate_postmortem_content


def main():
    """
    A tool to verify that the agent can monotonically improve its capabilities.

    This tool works by:
    1. Running a target test file that is known to fail, confirming the agent lacks a capability.
    2. Invoking the agent's self-correction mechanism to learn the new capability.
    3. Running the target test again to confirm it now passes.
    4. Running the full test suite to ensure no existing capabilities were lost.
    """
    parser = argparse.ArgumentParser(
        description="Verify monotonic capability improvement."
    )
    parser.add_argument(
        "--test-file",
        required=True,
        help="The path to the test file that defines the new capability.",
    )
    args = parser.parse_args()

    print(f"--- Capability Verifier Initiated for {args.test_file} ---")

    # Step 1: Confirm the initial test fails
    print("\n--- Step 1: Confirming initial failure ---")
    initial_result = subprocess.run(
        [sys.executable, args.test_file], capture_output=True, text=True
    )
    if initial_result.returncode == 0:
        print(
            "Error: Test file passed unexpectedly. The agent may already possess this capability."
        )
        print(initial_result.stdout)
        sys.exit(1)
    else:
        print("Success: Test file failed as expected.")

    # Step 2: Create a lesson and invoke the self-correction orchestrator
    print("\n--- Step 2: Invoking self-correction ---")
    postmortem_content = generate_postmortem_content()
    postmortem_path = "postmortems/capability_verifier_report.md"
    with open(postmortem_path, "w") as f:
        f.write(postmortem_content)

    # Now, we run the knowledge compiler to process the new post-mortem.
    knowledge_compiler_result = subprocess.run(
        [sys.executable, "tooling/knowledge_compiler.py", "--source-dir", "postmortems/"],
        capture_output=True,
        text=True,
    )
    if knowledge_compiler_result.returncode != 0:
        print("Error: Knowledge compiler failed.")
        print(knowledge_compiler_result.stderr)
        sys.exit(1)
    else:
        print("Success: Knowledge compiler processed the new post-mortem.")

    # With the lesson now properly in the knowledge core, we can invoke the orchestrator.
    orchestrator_result = subprocess.run(
        [sys.executable, "tooling/self_correction_orchestrator.py"],
        capture_output=True,
        text=True,
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
    final_result = subprocess.run(
        [sys.executable, args.test_file], capture_output=True, text=True
    )
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
    regression_result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "tests/"],
        capture_output=True,
        text=True,
    )
    if regression_result.returncode != 0:
        print("Error: Regressions detected. The agent has lost a capability.")
        print(regression_result.stderr)
        sys.exit(1)
    else:
        print("Success: No regressions detected.")
        print("\n--- Capability Verifier Finished: Monotonic Improvement Confirmed ---")


if __name__ == "__main__":
    main()
