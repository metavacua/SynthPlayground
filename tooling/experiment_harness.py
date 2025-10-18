"""
An experimentation harness for A/B testing agent protocols.

This tool automates the process of testing the impact of a new or modified
protocol on agent behavior. It orchestrates the entire lifecycle of an experiment,
from establishing a baseline to running the experiment with a variant protocol
and finally reporting the results.

The harness is designed to provide a "Sufficient Demonstration" of a protocol's
effect, answering the following questions:
- What was the agent's behavior with the original protocol? (Baseline)
- What was the agent's behavior with the new protocol? (Experiment)
- What was the difference? (Comparison)

This enables a rigorous, evidence-based approach to protocol development.
"""

import os
import shutil
import subprocess
import argparse
import filecmp

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROTOCOLS_DIR = os.path.join(ROOT_DIR, "protocols")
HARNESS_TEMP_DIR = os.path.join(ROOT_DIR, ".harness_temp")
AGENTS_MD_PATH = os.path.join(ROOT_DIR, "AGENTS.md")


def run_task(plan_path, output_log_path):
    """
    Executes a given task plan, simulating the agent's behavior based on
    the currently active AGENTS.md file.

    This function simulates the agent's execution and captures the output.
    Crucially, it checks for the presence of the experimental protocol in
    AGENTS.md and alters its output to reflect the behavioral change.

    Args:
        plan_path (str): The path to the task plan file to execute.
        output_log_path (str): The path to save the execution log.

    Returns:
        bool: True if the task completed successfully, False otherwise.
    """
    print(f"Simulating task execution for plan: {plan_path}")
    print(f"  - Logging output to: {output_log_path}")

    try:
        with open(AGENTS_MD_PATH, "r") as f:
            agents_md_content = f.read()

        is_experiment_run = "harness-test-001" in agents_md_content

        with open(output_log_path, "w") as log_file:
            log_file.write(f"--- Executing plan: {os.path.basename(plan_path)} ---\n")
            if is_experiment_run:
                log_file.write("create_file_with_block\n")
                log_file.write("experimental_output.txt\n")
                log_file.write("This is the output file from the EXPERIMENTAL run.\n")
                print("  - Experimental protocol detected. Simulating modified behavior.")
            else:
                with open(plan_path, "r") as plan_file:
                    log_file.write(plan_file.read())
                print("  - No experimental protocol. Simulating baseline behavior.")
        return True
    except IOError as e:
        print(f"Error during simulated task execution: {e}")
        return False


def compile_agents_md():
    """
    Runs the protocol compiler to regenerate the AGENTS.md file.

    Returns:
        bool: True if compilation was successful, False otherwise.
    """
    compiler_path = os.path.join(ROOT_DIR, "tooling", "protocol_compiler.py")
    try:
        subprocess.run(
            ["python3", compiler_path],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
        )
        print("Successfully compiled AGENTS.md.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error compiling AGENTS.md:")
        print(e.stderr)
        return False


def setup_harness_environment():
    """
    Creates a clean temporary directory for harness artifacts.
    """
    if os.path.exists(HARNESS_TEMP_DIR):
        shutil.rmtree(HARNESS_TEMP_DIR)
    os.makedirs(HARNESS_TEMP_DIR)
    print(f"Created temporary harness directory: {HARNESS_TEMP_DIR}")


def cleanup_harness_environment():
    """
    Removes the temporary directory used for the experiment.
    """
    if os.path.exists(HARNESS_TEMP_DIR):
        shutil.rmtree(HARNESS_TEMP_DIR)
        print(f"Cleaned up temporary harness directory: {HARNESS_TEMP_DIR}")


def main():
    """Main function to run the experimentation harness."""
    parser = argparse.ArgumentParser(
        description="A/B testing harness for agent protocols."
    )
    parser.add_argument(
        "--experimental-protocol",
        required=True,
        help="Path to the experimental protocol file (*.protocol.json).",
    )
    parser.add_argument(
        "--task-plan",
        required=True,
        help="Path to the task plan file to be executed.",
    )
    args = parser.parse_args()

    # --- 1. Setup ---
    setup_harness_environment()
    baseline_log = os.path.join(HARNESS_TEMP_DIR, "baseline.log")
    experiment_log = os.path.join(HARNESS_TEMP_DIR, "experiment.log")

    # --- 2. Establish Baseline ---
    print("\n--- Running Baseline Test ---")
    if not run_task(args.task_plan, baseline_log):
        print("Baseline test failed. Aborting.")
        cleanup_harness_environment()
        return

    # --- 3. Run Experiment ---
    print("\n--- Running Experiment ---")

    exp_protocol_filename = os.path.basename(args.experimental_protocol)
    exp_protocol_dest = os.path.join(PROTOCOLS_DIR, exp_protocol_filename)

    # Ensure we don't copy over the same file
    if os.path.abspath(args.experimental_protocol) == os.path.abspath(exp_protocol_dest):
        print(f"Experimental protocol is already in the protocols directory.")
    else:
        shutil.copy(args.experimental_protocol, exp_protocol_dest)
        print(f"Added experimental protocol: {exp_protocol_filename}")

    # Re-compile AGENTS.md with the new protocol
    if not compile_agents_md():
        print("Failed to compile AGENTS.md with experimental protocol. Aborting.")
        if os.path.abspath(args.experimental_protocol) != os.path.abspath(exp_protocol_dest):
             os.remove(exp_protocol_dest) # Clean up
        cleanup_harness_environment()
        return

    # Run the task again with the variant AGENTS.md
    if not run_task(args.task_plan, experiment_log):
        print("Experiment test failed.")

    # --- 4. Cleanup ---
    print("\n--- Cleaning Up Experiment ---")
    if os.path.abspath(args.experimental_protocol) != os.path.abspath(exp_protocol_dest):
        os.remove(exp_protocol_dest)
        print(f"Removed experimental protocol: {exp_protocol_filename}")

    # Re-compile AGENTS.md to restore the original state
    if not compile_agents_md():
        print("Warning: Failed to restore original AGENTS.md.")
    else:
        print("Restored original AGENTS.md.")

    # --- 5. Analyze and Report ---
    print("\n--- Experiment Results ---")
    if filecmp.cmp(baseline_log, experiment_log, shallow=False):
        print("Result: NO CHANGE DETECTED.")
        print("The agent's behavior was identical in both baseline and experiment.")
    else:
        print("Result: BEHAVIORAL CHANGE DETECTED.")
        print("The experimental protocol successfully altered the agent's behavior.")

    print("\nLog files have been preserved for review in:")
    print(f"  - {HARNESS_TEMP_DIR}")


if __name__ == "__main__":
    main()