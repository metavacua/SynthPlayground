import os
import shutil
import subprocess
import json

# Define paths
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
AGENT_SMITH_DIR = os.path.join(ROOT_DIR, 'agent_smith')
SANDBOX_DIR = os.path.join(AGENT_SMITH_DIR, 'experiment_sandbox')
PROTOCOLS_SRC_DIR = os.path.join(ROOT_DIR, 'protocols')
TOOLING_SRC_DIR = os.path.join(ROOT_DIR, 'tooling')
UTILS_SRC_DIR = os.path.join(ROOT_DIR, 'utils')

def main():
    """
    Main function to set up sandbox, mutate protocols, and compile a new AGENTS.md.
    """
    print("--- Starting AGENTS.md Variant Generation ---")

    # 1. Set up the sandbox
    setup_sandbox()

    # 2. Perform a meaningful mutation
    mutate_protocols()

    # 3. Compile the new AGENTS.md variant
    compile_variant()

    print("--- AGENTS.md Variant Generation Complete ---")
    print(f"New variant generated at: {os.path.join(SANDBOX_DIR, 'AGENTS.md')}")

def setup_sandbox():
    """
    Creates a clean sandbox directory and copies necessary compiler files and their
    dependencies into it.
    """
    print(f"Setting up sandbox at: {SANDBOX_DIR}")
    if os.path.exists(SANDBOX_DIR):
        shutil.rmtree(SANDBOX_DIR)
    os.makedirs(SANDBOX_DIR)

    # Copy protocols, tooling, and utils directories
    shutil.copytree(PROTOCOLS_SRC_DIR, os.path.join(SANDBOX_DIR, 'protocols'))
    shutil.copytree(TOOLING_SRC_DIR, os.path.join(SANDBOX_DIR, 'tooling'))
    shutil.copytree(UTILS_SRC_DIR, os.path.join(SANDBOX_DIR, 'utils'))

    print("Sandbox created and all source directories copied.")

def mutate_protocols():
    """
    Applies a specific, meaningful mutation to the protocol files in the sandbox.
    """
    # For this demonstration, we will add a rule to forbid 'list_files'.
    # We'll add this to the 'interaction.protocol.json' protocol file.
    mutation_target_path = os.path.join(SANDBOX_DIR, 'protocols', 'interaction.protocol.json')

    print(f"Applying mutation to: {mutation_target_path}")

    # Use the json library to parse and modify the protocol file.
    with open(mutation_target_path, 'r') as f:
        protocol_data = json.load(f)

    # Define the new rule as a Python dictionary
    new_rule = {
      "rule_id": "forbid-list-files-experiment",
      "description": "The agent is forbidden from using the `list_files` tool for this experiment.",
      "enforcement": "This is a hardcoded rule for the experimental protocol."
    }

    # Append the new rule to the list of rules
    if "rules" in protocol_data and isinstance(protocol_data["rules"], list):
        protocol_data["rules"].append(new_rule)
    else:
        raise RuntimeError(f"Could not find a 'rules' list in {mutation_target_path}")

    # Write the modified data back to the file with pretty printing
    with open(mutation_target_path, 'w') as f:
        json.dump(protocol_data, f, indent=2)

    print("Mutation applied successfully: 'list_files' is now forbidden.")


def compile_variant():
    """
    Executes the hierarchical compiler within the sandbox to build the new AGENTS.md.
    """
    print("Compiling new AGENTS.md variant...")
    compiler_script_path = os.path.join('tooling', 'hierarchical_compiler.py')

    # Run the compiler from within the sandbox directory.
    # The CWD is the sandbox root, which allows python to find the 'tooling' and 'utils' packages.
    process = subprocess.run(
        ['python3', compiler_script_path],
        cwd=SANDBOX_DIR,
        capture_output=True,
        text=True
    )

    if process.returncode != 0:
        print("--- COMPILER ERROR ---")
        print(process.stdout)
        print(process.stderr)
        raise RuntimeError("Failed to compile the AGENTS.md variant.")

    print("Compiler executed successfully.")
    print(process.stdout) # Show compiler output for verification

if __name__ == "__main__":
    main()