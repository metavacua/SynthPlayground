import os
import shutil
import subprocess
import argparse
import glob

def log_step(message):
    """Prints a formatted step message."""
    print(f"\n--- {message} ---")

def evaluate_fitness(sandbox_path, test_suite_dir):
    """
    Evaluates the fitness of the AGENTS.md variant by running a suite of test subjects.

    Args:
        sandbox_path (str): The path to the sandbox directory.
        test_suite_dir (str): Path to the directory containing test subjects.

    Returns:
        int: The fitness score, calculated as a percentage of tests passed.
    """
    log_step(f"Evaluating fitness of variant in: {sandbox_path}")

    test_subjects = glob.glob(os.path.join(test_suite_dir, "test_subject_*.py"))
    if not test_subjects:
        print(f"ERROR: No test subjects found in {test_suite_dir}")
        return 0

    passed_tests = 0
    total_tests = len(test_subjects)

    for test_path in test_subjects:
        test_name = os.path.basename(test_path)
        log_step(f"Running test: {test_name}")

        # This is where the agent would be invoked to fix the bug.
        # For this simulation, we will copy the *unfixed* test subject
        # into the sandbox and run it. A real test would involve
        # copying the test, running the agent, and then running the (hopefully fixed) test.
        shutil.copy(test_path, sandbox_path)
        sandboxed_test_path = os.path.join(sandbox_path, test_name)

        try:
            result = subprocess.run(
                ["python3", sandboxed_test_path],
                capture_output=True,
                text=True,
                check=False,
                cwd=sandbox_path
            )
            output = result.stdout.strip()

            # The success condition is that the script's output contains "SUCCESS"
            if "SUCCESS" in output:
                passed_tests += 1
                print(f"  - Result: PASS")
            else:
                print(f"  - Result: FAIL (Output: {output})")

        except Exception as e:
            print(f"  - Result: ERROR ({e})")

    if total_tests == 0:
        return 0

    fitness_score = (passed_tests / total_tests) * 100
    print(f"\nTest Suite Summary: {passed_tests} / {total_tests} tests passed.")
    return int(fitness_score)

def main():
    """Main function to orchestrate the fitness evaluation."""
    parser = argparse.ArgumentParser(description="Agent Smith: Polymorphic Fitness Evaluator")
    parser.add_argument(
        "--sandbox",
        required=True,
        help="The path to the sandbox directory containing the AGENTS.variant.md."
    )
    parser.add_argument(
        "--test-suite-dir",
        required=True,
        help="The path to the directory containing the test subject scripts."
    )
    args = parser.parse_args()

    fitness_score = evaluate_fitness(args.sandbox, args.test_suite_dir)
    print(f"\nFinal Polymorphic Fitness Score: {fitness_score}")

if __name__ == "__main__":
    main()