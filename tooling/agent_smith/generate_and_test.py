import os
import shutil
import subprocess
import sys
import argparse

# --- Configuration ---
# Set the sandbox directory name at the top level of the repo
SANDBOX_DIR_NAME = "agent_smith_sandbox"
# The name for the generated variant AGENTS.md
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
            command, check=True, capture_output=True, text=True, cwd=cwd
        )
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
        print("Sandbox already exists. Deleting it for a clean start.")
        shutil.rmtree(sandbox_path)
    os.makedirs(sandbox_path)
    print("Sandbox created successfully.")


def copy_sources(root_dir, sandbox_path):
    """Copies the necessary source files and compiler into the sandbox."""
    log_step("Copying protocol sources and compiler to sandbox")

    # Define source and destination paths
    source_protocols_dir = os.path.join(root_dir, "protocols")
    dest_protocols_dir = os.path.join(sandbox_path, "protocols")

    source_compliance_dir = os.path.join(root_dir, "compliance")
    dest_compliance_dir = os.path.join(sandbox_path, "compliance")

    source_compiler_dir = os.path.join(root_dir, "tooling")
    dest_compiler_dir = os.path.join(sandbox_path, "tooling")

    source_utils_dir = os.path.join(root_dir, "utils")
    dest_utils_dir = os.path.join(sandbox_path, "utils")

    # Perform the copy operations
    shutil.copytree(source_protocols_dir, dest_protocols_dir, dirs_exist_ok=True)
    shutil.copytree(source_compliance_dir, dest_compliance_dir, dirs_exist_ok=True)

    # We need to copy the whole tooling and utils directories for the compiler to work
    shutil.copytree(source_compiler_dir, dest_compiler_dir, dirs_exist_ok=True)
    shutil.copytree(source_utils_dir, dest_utils_dir, dirs_exist_ok=True)

    print("Sources copied successfully.")
    return True


def install_dependencies(sandbox_path):
    """Installs dependencies from requirements.txt into the sandbox."""
    log_step("Installing dependencies in sandbox")
    requirements_path = os.path.join(sandbox_path, "tooling", "requirements.txt")
    if not os.path.exists(requirements_path):
        print("ERROR: requirements.txt not found in sandboxed tooling directory.")
        return False

    # It's better to install to a target directory within the sandbox to avoid polluting the system
    pip_target_dir = os.path.join(sandbox_path, ".pip_dependencies")
    os.makedirs(pip_target_dir, exist_ok=True)

    command = ["pip", "install", "-r", requirements_path, "--target", pip_target_dir]

    # We run pip from the sandbox root
    if not run_command(command, cwd=sandbox_path):
        print("ERROR: Failed to install dependencies.")
        return False

    print("Dependencies installed successfully.")
    return pip_target_dir


def apply_mutation(sandbox_path, mutation_target):
    """Applies the specified mutation to the sandboxed sources."""
    log_step(f"Applying mutation: Deleting '{mutation_target}'")
    target_file = os.path.join(sandbox_path, mutation_target)

    if os.path.exists(target_file):
        os.remove(target_file)
        # Also remove the markdown version if it exists
        md_target_file = target_file.replace(".protocol.json", ".protocol.md")
        if os.path.exists(md_target_file):
            os.remove(md_target_file)
        print(f"Successfully deleted: {target_file} (and its .md pair)")
        return True
    else:
        print(f"ERROR: Mutation target not found: {target_file}")
        return False


def compile_variant(sandbox_path, python_path_ext):
    """Runs the hierarchical compiler inside the sandbox."""
    log_step("Compiling the AGENTS.md variant")
    compiler_script = os.path.join(sandbox_path, "tooling", "hierarchical_compiler.py")

    # Add the installed dependencies to the Python path
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{python_path_ext}{os.pathsep}{env.get('PYTHONPATH', '')}"

    command = ["python3", compiler_script]

    log_step(f"Executing: {' '.join(command)} with updated PYTHONPATH")
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=sandbox_path,
            env=env,
        )
        print("Output:\n" + result.stdout)
        if result.stderr:
            print("Stderr:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}")
        print("Stderr:\n" + e.stderr)
        print("Stdout:\n" + e.stdout)
        return None

    # The compiler creates AGENTS.md at the root of the sandbox
    compiled_agents_md = os.path.join(sandbox_path, "AGENTS.md")
    variant_path = os.path.join(sandbox_path, VARIANT_AGENTS_MD_NAME)

    if os.path.exists(compiled_agents_md):
        os.rename(compiled_agents_md, variant_path)
        print(f"Successfully compiled and renamed to {variant_path}")
        return variant_path
    else:
        print("ERROR: Compiled AGENTS.md not found in sandbox.")
        return None


def verify_variant(variant_path, mutation_check_string):
    """Performs a basic verification to check the variant was created correctly."""
    log_step(f"Verifying the generated variant: {variant_path}")
    if not os.path.exists(variant_path):
        print("FAIL: Variant file was not created.")
        return False

    with open(variant_path, "r") as f:
        content = f.read()

    if mutation_check_string in content:
        print(
            f"FAIL: Verification check string '{mutation_check_string}' was found in the variant."
        )
        return False
    else:
        print(
            f"PASS: Verification check string '{mutation_check_string}' was NOT found. Mutation was successful."
        )
        return True


def cleanup_sandbox(sandbox_path):
    """Deletes the sandbox directory."""
    log_step(f"Cleaning up sandbox: {sandbox_path}")
    if os.path.exists(sandbox_path):
        shutil.rmtree(sandbox_path)
        print("Sandbox cleaned successfully.")
    else:
        print("Sandbox not found, no cleanup needed.")


def main():
    """Main function to orchestrate the generation and testing process."""
    parser = argparse.ArgumentParser(
        description="Agent Smith: AGENTS.md Variant Generator"
    )
    parser.add_argument(
        "--mutate-delete",
        required=True,
        help="The path of the protocol file to delete (relative to repo root).",
    )
    parser.add_argument(
        "--verify-not-present",
        required=True,
        help="A string that should NOT be present in the final compiled variant.",
    )
    args = parser.parse_args()

    root_dir = get_repo_root()
    sandbox_path = os.path.join(root_dir, SANDBOX_DIR_NAME)

    try:
        create_sandbox(root_dir, sandbox_path)

        if not copy_sources(root_dir, sandbox_path):
            raise RuntimeError("Failed to copy sources to sandbox.")

        pip_path = install_dependencies(sandbox_path)
        if not pip_path:
            raise RuntimeError("Failed to install dependencies.")

        if not apply_mutation(sandbox_path, args.mutate_delete):
            raise RuntimeError("Failed to apply mutation.")

        variant_path = compile_variant(sandbox_path, pip_path)
        if not variant_path:
            raise RuntimeError("Failed to compile the variant.")

        if not verify_variant(variant_path, args.verify_not_present):
            raise RuntimeError("Variant failed verification.")

        print("\nSUCCESS: AGENTS.md variant generated and verified successfully.")
        print(f"The variant is located at: {variant_path}")
        print(
            "The sandbox will be left for inspection. Run with --cleanup to remove it."
        )

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # In case of failure, still try to clean up
        cleanup_sandbox(sandbox_path)
        sys.exit(1)
    # Note: We are not cleaning up on success so the agent can use the sandbox.
    # A final 'cleanup' command would be needed in a real workflow.


if __name__ == "__main__":
    main()
