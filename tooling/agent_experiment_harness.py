"""
Orchestrates an experiment on agent protocols.

This script provides a framework for testing how a change to a protocol
affects the agent's behavior. It automates the process of:
1. Creating a variant of a protocol file using `protocol_mutator.py`.
2. Compiling a new `AGENTS.variant.md` file from this modified protocol.
3. Setting up a dedicated directory for the experiment's artifacts.

Example Usage:
python tooling/agent_experiment_harness.py \
  --source_protocol protocols/some_protocol.protocol.json \
  --mutation 'ADD_RULE:{"rule_id": "new-rule", ...}' \
  --experiment_name 'my-test-experiment'
"""

import os
import subprocess
import argparse
import sys
import shutil

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXPERIMENTS_DIR = os.path.join(ROOT_DIR, "experiments")

def run_command(command):
    """Runs a command in the shell and exits if it fails."""
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {' '.join(command)}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Orchestrates an agent protocol experiment.")
    parser.add_argument(
        "--source_protocol",
        required=True,
        help="The source protocol file to mutate (e.g., 'protocols/core/some_protocol.protocol.json')."
    )
    parser.add_argument(
        "--mutation",
        required=True,
        help="The mutation to apply to the source protocol."
    )
    parser.add_argument(
        "--experiment_name",
        required=True,
        help="A unique name for the experiment. This will be used as the directory name for the artifacts."
    )
    parser.add_argument(
        "--base_protocols_dir",
        default="protocols",
        help="The base directory of protocols to use for the experiment."
    )

    args = parser.parse_args()

    # --- 1. Setup Experiment Directory ---
    experiment_path = os.path.join(EXPERIMENTS_DIR, args.experiment_name)
    variant_protocols_path = os.path.join(experiment_path, "protocols")

    print(f"--- Starting Experiment: {args.experiment_name} ---")
    print(f"Creating experiment directory at: {experiment_path}")

    # Clean up old experiment directory if it exists
    if os.path.exists(experiment_path):
        shutil.rmtree(experiment_path)

    # Copy the entire base protocols directory to the experiment folder
    # This ensures our experiment runs in an isolated protocol set
    shutil.copytree(args.base_protocols_dir, variant_protocols_path)
    print(f"Copied base protocols from '{args.base_protocols_dir}' to '{variant_protocols_path}'")

    # --- 2. Mutate the Protocol ---
    # The path to the protocol *inside the new experiment directory*
    target_protocol_in_experiment = os.path.join(variant_protocols_path, os.path.basename(args.source_protocol))

    mutator_script = os.path.join(ROOT_DIR, "tooling", "protocol_mutator.py")
    mutation_command = [
        sys.executable,
        mutator_script,
        "--source",
        target_protocol_in_experiment, # We mutate the copied file
        "--output",
        target_protocol_in_experiment, # Overwrite the copied file with the mutated version
        "--mutation",
        args.mutation
    ]
    run_command(mutation_command)

    # --- 3. Compile the Variant AGENTS.md ---
    compiler_script = os.path.join(ROOT_DIR, "tooling", "protocol_compiler.py")
    variant_agents_md_path = os.path.join(experiment_path, "AGENTS.variant.md")

    compiler_command = [
        sys.executable,
        compiler_script,
        "--source-dir",
        variant_protocols_path,
        "--output-file",
        variant_agents_md_path
    ]
    run_command(compiler_command)

    print(f"\n--- Experiment Setup Complete ---")
    print(f"Variant AGENTS.md generated at: {variant_agents_md_path}")
    print("You can now run an agent against this variant to test its behavior.")

if __name__ == "__main__":
    main()