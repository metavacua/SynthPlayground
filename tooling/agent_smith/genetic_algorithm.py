import os
import shutil
import subprocess
import argparse

def log_header(message):
    """Prints a formatted header message."""
    print("\n" + "="*60)
    print(f" {message}")
    print("="*60 + "\n")

def run_script(command):
    """Runs a script in a subprocess and returns True on success."""
    print(f"Executing: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, capture_output=False, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Script failed with exit code {e.returncode}")
        return False

def get_fitness(sandbox_path, success_string):
    """Runs the fitness evaluator and returns the score."""
    command = [
        "python3", "tooling/agent_smith/fitness_evaluator.py",
        "--sandbox", sandbox_path,
        "--success-string", success_string
    ]
    # We need to capture output to get the score
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Fitness Score:" in line:
            return int(line.split(":")[1].strip())
    return 0

def main():
    """Main function to orchestrate the genetic algorithm."""

    # --- 1. Define the Genetic Experiment ---
    log_header("Initializing Genetic Algorithm Experiment")

    # The "gene" we want to introduce.
    target_protocol_file = "protocols/00_bootstrap.protocol.json"
    target_rule_id = "bootstrap-load-agents-md"
    field_to_mutate = "description"
    new_gene_value = "This is the evolved description that proves the mutation worked."

    # The success condition for our fitness function.
    success_string = new_gene_value

    # --- 2. Evaluate the Baseline (Parent) ---
    log_header("Step 1: Evaluating Fitness of Baseline (Parent)")
    parent_sandbox = "agent_smith_sandbox_parent"

    # Create the baseline variant (no mutation)
    compiler_command_parent = [
        "python3", "tooling/agent_smith/compiler_harness.py",
        "--sandbox-name", parent_sandbox,
        # No mutation arguments are passed
    ]
    if not run_script(compiler_command_parent):
        print("FATAL: Could not compile the parent variant.")
        exit(1)

    # Evaluate the parent's fitness
    parent_fitness = get_fitness(parent_sandbox, success_string)
    print(f"\nParent Fitness Score: {parent_fitness}")
    assert parent_fitness == 0, "Parent should have 0 fitness as it lacks the gene."
    print("Baseline evaluation successful. Parent is not fit, as expected.")


    # --- 3. Create and Evaluate the Offspring ---
    log_header("Step 2: Creating and Evaluating Mutated Offspring")
    offspring_sandbox = "agent_smith_sandbox_offspring"

    # Create the mutated offspring variant
    compiler_command_offspring = [
        "python3", "tooling/agent_smith/compiler_harness.py",
        "--sandbox-name", offspring_sandbox,
        "--mutate-json-file", target_protocol_file,
        "--mutate-rule-id", target_rule_id,
        "--mutate-field", field_to_mutate,
        "--mutate-value", new_gene_value
    ]
    if not run_script(compiler_command_offspring):
        print("FATAL: Could not compile the offspring variant.")
        exit(1)

    # Evaluate the offspring's fitness
    offspring_fitness = get_fitness(offspring_sandbox, success_string)
    print(f"\nOffspring Fitness Score: {offspring_fitness}")
    assert offspring_fitness == 100, "Offspring should be 100% fit as it has the gene."
    print("Offspring evaluation successful. Offspring is fit, as expected.")


    # --- 4. Selection ---
    log_header("Step 3: Selection")
    if offspring_fitness > parent_fitness:
        winner = "Offspring"
        winner_fitness = offspring_fitness
    else:
        winner = "Parent"
        winner_fitness = parent_fitness

    print(f"Selection complete. The winner is the {winner} with a fitness of {winner_fitness}.")
    print("\nGenetic Algorithm cycle complete and successful.")

    # --- 5. Cleanup ---
    log_header("Step 4: Cleaning up sandboxes")
    shutil.rmtree(parent_sandbox, ignore_errors=True)
    shutil.rmtree(offspring_sandbox, ignore_errors=True)
    print("Sandboxes cleaned.")


if __name__ == "__main__":
    main()