import os
import shutil
import subprocess
import sys
import argparse

# --- Configuration ---
VARIANT_AGENTS_MD_NAME = "AGENTS.variant.md"

def get_repo_root():
    """Gets the absolute path of the repository root."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def log_step(message):
    """Prints a formatted step message."""
    print(f"\n--- {message} ---")

def run_command(command, cwd):
    """Runs a command in a subprocess and handles errors."""
    log_step(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        # Don't print stdout/stderr for pip install unless there's an error
        if "pip install" not in " ".join(command):
            print("Output:\n" + result.stdout)
            if result.stderr:
                print("Stderr:\n" + result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}")
        print("Stderr:\n" + e.stderr)
        print("Stdout:\n" + e.stdout)
        return False

def create_sandbox(root_dir, sandbox_path):
    """Creates a clean sandbox directory."""
    log_step(f"Creating sandbox at: {sandbox_path}")
    if os.path.exists(sandbox_path):
        shutil.rmtree(sandbox_path)
    os.makedirs(sandbox_path)
    print("Sandbox created successfully.")

def copy_sources(root_dir, sandbox_path):
    """Copies the necessary source files and compiler into the sandbox."""
    log_step("Copying protocol sources and compiler to sandbox")

    # Define source and destination paths
    shutil.copytree(os.path.join(root_dir, "protocols"), os.path.join(sandbox_path, "protocols"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(root_dir, "compliance"), os.path.join(sandbox_path, "compliance"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(root_dir, "tooling"), os.path.join(sandbox_path, "tooling"), dirs_exist_ok=True)
    shutil.copytree(os.path.join(root_dir, "utils"), os.path.join(sandbox_path, "utils"), dirs_exist_ok=True)

    print("Sources copied successfully.")
    return True

def install_dependencies(sandbox_path):
    """Installs dependencies from requirements.txt into the sandbox."""
    log_step("Installing dependencies in sandbox")
    requirements_path = os.path.join(sandbox_path, "tooling", "requirements.txt")
    pip_target_dir = os.path.join(sandbox_path, ".pip_dependencies")
    os.makedirs(pip_target_dir, exist_ok=True)

    command = ["pip", "install", "-r", requirements_path, "--target", pip_target_dir]

    if not run_command(command, cwd=sandbox_path):
        return None

    print("Dependencies installed successfully.")
    return pip_target_dir

def apply_mutation(sandbox_path, args):
    """Applies a mutation to the sandboxed sources using mutator.py."""
    if not args.mutate_json_file:
        log_step("No mutation requested. Skipping mutation step.")
        return True

    log_step("Applying mutation via mutator.py")
    mutator_script = os.path.join(sandbox_path, "tooling", "agent_smith", "mutator.py")
    target_file_in_sandbox = os.path.join(sandbox_path, args.mutate_json_file)

    command = [
        "python3", mutator_script,
        "--file", target_file_in_sandbox,
        "--rule-id", args.mutate_rule_id,
        "--field", args.mutate_field,
        "--value", args.mutate_value
    ]

    return run_command(command, cwd=sandbox_path)


def compile_variant(sandbox_path, python_path_ext):
    """Runs the hierarchical compiler inside the sandbox."""
    log_step("Compiling the AGENTS.md variant")
    compiler_script = os.path.join(sandbox_path, "tooling", "hierarchical_compiler.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{python_path_ext}{os.pathsep}{env.get('PYTHONPATH', '')}"

    command = ["python3", compiler_script]

    # We need to run this from the sandbox root for paths to work correctly
    if not run_command(command, cwd=sandbox_path):
        return None

    compiled_agents_md = os.path.join(sandbox_path, "AGENTS.md")
    variant_path = os.path.join(sandbox_path, VARIANT_AGENTS_MD_NAME)

    if os.path.exists(compiled_agents_md):
        os.rename(compiled_agents_md, variant_path)
        print(f"Successfully compiled and renamed to {variant_path}")
        return variant_path
    else:
        print("ERROR: Compiled AGENTS.md not found in sandbox.")
        return None

def main():
    """Main function to orchestrate the generation and testing process."""
    parser = argparse.ArgumentParser(description="Agent Smith: Compiler Harness")
    parser.add_argument("--sandbox-name", required=True, help="The name of the sandbox directory to create.")
    # Mutation arguments are now optional
    parser.add_argument("--mutate-json-file", help="The path of the .protocol.json file to mutate (relative to repo root).")
    parser.add_argument("--mutate-rule-id", help="The ID of the rule to mutate.")
    parser.add_argument("--mutate-field", help="The field within the rule to change.")
    parser.add_argument("--mutate-value", help="The new value for the specified field.")
    args = parser.parse_args()

    root_dir = get_repo_root()
    sandbox_path = os.path.join(root_dir, args.sandbox_name)

    try:
        create_sandbox(root_dir, sandbox_path)

        if not copy_sources(root_dir, sandbox_path):
            raise RuntimeError("Failed to copy sources to sandbox.")

        pip_path = install_dependencies(sandbox_path)
        if not pip_path:
            raise RuntimeError("Failed to install dependencies.")

        if not apply_mutation(sandbox_path, args):
            raise RuntimeError("Failed to apply mutation.")

        variant_path = compile_variant(sandbox_path, pip_path)
        if not variant_path:
            raise RuntimeError("Failed to compile the variant.")

        print(f"\nSUCCESS: AGENTS.md variant generated successfully in {sandbox_path}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # In case of failure, still try to clean up
        shutil.rmtree(sandbox_path, ignore_errors=True)
        sys.exit(1)

if __name__ == "__main__":
    main()