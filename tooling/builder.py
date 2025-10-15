"""
This script provides a unified, configuration-driven build system for the project.

It reads a central `build_config.json` file to determine which compilers or
generators to run for different build targets (like 'docs', 'agents', etc.).
This allows for a flexible and easily extensible build process without modifying
the build script itself. New targets can be added simply by updating the JSON
configuration.

The script supports building individual targets, listing all available targets,
and building all targets in a predefined, logical order. It captures and
displays the output of each build step, providing clear success or failure
reporting.
"""
import os
import json
import argparse
import subprocess
from datetime import datetime

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_FILE = os.path.join(ROOT_DIR, "build_config.json")


def load_config():
    """Loads the build configuration file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Build config file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def execute_build(target_name, config):
    """
    Executes the build process for a specific target defined in the config.
    """
    if target_name not in config["targets"]:
        raise ValueError(f"Target '{target_name}' not found in build configuration.")

    target_config = config["targets"][target_name]
    compiler_path = os.path.join(ROOT_DIR, target_config["compiler"])
    output_path = os.path.join(ROOT_DIR, target_config["output"])

    command = ["python3", compiler_path]

    # Handle different source types
    if target_name == "agents":
        # The hierarchical compiler discovers its own sources.
        pass
    elif target_name == "readme":
        # The readme generator takes a single source file.
        source_file = os.path.join(ROOT_DIR, target_config["sources"][0])
        command.extend(["--source-file", source_file, "--output-file", output_path])
    else:
        # Most compilers take a source directory.
        source_dir = os.path.join(ROOT_DIR, target_config["sources"][0])
        command.extend(["--source-dir", source_dir, "--output-file", output_path])

    # Add any additional command-line options
    if "options" in target_config:
        for option, value in target_config["options"].items():
            command.extend([option, os.path.join(ROOT_DIR, value)])

    print(f"--- Building Target: {target_name.upper()} ---")
    print(f"  - Compiler: {target_config['compiler']}")
    if 'output' in target_config:
        print(f"  - Output:   {target_config['output']}")
    print(f"  - Command:  {' '.join(command)}")

    try:
        start_time = datetime.now()
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, cwd=ROOT_DIR
        )
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print("  - Status:   SUCCESS")
        print(f"  - Duration: {duration:.2f}s")
        if result.stdout:
            print("  - STDOUT:")
            for line in result.stdout.strip().split("\n"):
                print(f"    {line}")
        if result.stderr:
            print("  - STDERR:")
            for line in result.stderr.strip().split("\n"):
                print(f"    {line}")
    except subprocess.CalledProcessError as e:
        print("  - Status:   FAILURE")
        print(
            f"  - Error:    Build process for '{target_name}' failed with exit code {e.returncode}."
        )
        print("  - STDERR:")
        for line in e.stderr.strip().split("\n"):
            print(f"    {line}")
        raise  # Re-raise the exception to halt the build if a step fails


def main():
    """
    Main function to parse arguments and drive the build process.
    """
    parser = argparse.ArgumentParser(
        description="Unified build script for the project."
    )
    parser.add_argument(
        "--target",
        "-t",
        required=True,
        help="The build target to execute (e.g., 'docs', 'security', 'agents', 'all').",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="List all available build targets and exit.",
    )

    args = parser.parse_args()
    config = load_config()

    if args.list_targets:
        print("--- Available Build Targets ---")
        for name, details in config["targets"].items():
            print(
                f"  - {name}: {details.get('description', 'No description available.')}"
            )
        return

    if args.target == "all":
        print("--- Executing Full Build ---")
        # Build in a logical order
        build_order = ["docs", "security", "agents", "readme"]
        for target_name in build_order:
            if target_name in config["targets"]:
                execute_build(target_name, config)
            else:
                print(
                    f"Warning: Target '{target_name}' specified in 'all' but not found in config."
                )
        print("\n--- Full Build Finished ---")
    else:
        execute_build(args.target, config)
        print(f"\n--- Target '{args.target}' Finished ---")


if __name__ == "__main__":
    main()