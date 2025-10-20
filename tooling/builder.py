"""
A unified, configuration-driven build script for the project.

This script serves as the central entry point for all build-related tasks, such
as generating documentation, compiling protocols, and running code quality checks.
It replaces a traditional Makefile's direct command execution with a more
structured, maintainable, and introspectable approach.

The core logic is driven by a `build_config.json` file, which defines a series
of "targets." Each target specifies:
- The `type` of target: "compiler" or "command".
- For "compiler" types: `compiler` script, `output`, `sources`, and `options`.
- For "command" types: the `command` to execute.

The configuration also defines "build_groups", which are ordered collections of
targets (e.g., "all", "quality").

This centralized builder provides several advantages:
- **Single Source of Truth:** The `build_config.json` file is the definitive
  source for all build logic.
- **Consistency:** Ensures all build tasks are executed in a uniform way.
- **Extensibility:** New build targets can be added by simply updating the
  configuration file.
- **Discoverability:** The script can list all available targets and groups.
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


def execute_compiler_target(target_name, target_config):
    """Executes a 'compiler' type build target."""
    compiler_path = os.path.join(ROOT_DIR, target_config["compiler"])
    command = ["python3", compiler_path]

    # Handle sources
    if "sources" in target_config:
        for source in target_config["sources"]:
            # Check if it's a directory or a file
            if source.endswith("/"):
                command.extend(["--source-dir", os.path.join(ROOT_DIR, source)])
            else:
                command.extend(["--source-file", os.path.join(ROOT_DIR, source)])

    # Handle output
    if "output" in target_config:
        output_path = os.path.join(ROOT_DIR, target_config["output"])
        command.extend(["--output-file", output_path])

    # Handle options
    if "options" in target_config:
        for option, value in target_config["options"].items():
            # For options that are paths, join with ROOT_DIR
            if isinstance(value, str) and ("file" in option or "dir" in option):
                command.extend([option, os.path.join(ROOT_DIR, value)])
            else:
                command.extend([option, str(value)])

    return command, " ".join(command)


def execute_command_target(target_name, target_config):
    """Executes a 'command' type build target."""
    command_str = target_config["command"]
    return command_str, command_str


def execute_build(target_name, config):
    """Executes the build process for a specific target."""
    if target_name not in config["targets"]:
        raise ValueError(f"Target '{target_name}' not found in build configuration.")

    target_config = config["targets"][target_name]
    target_type = target_config.get("type", "compiler")  # Default to compiler

    print(f"--- Building Target: {target_name.upper()} ---")
    print(f"  - Type:     {target_type}")
    print(f"  - Desc:     {target_config.get('description', 'N/A')}")

    command = None
    command_str = ""
    shell = False

    if target_type == "compiler":
        command, command_str = execute_compiler_target(target_name, target_config)
    elif target_type == "command":
        command, command_str = execute_command_target(target_name, target_config)
        shell = True  # Shell commands run with shell=True
    else:
        raise ValueError(
            f"Unknown target type '{target_type}' for target '{target_name}'"
        )

    print(f"  - Command:  {command_str}")

    try:
        start_time = datetime.now()
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            shell=shell,
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
        print(f"  - Error:    Build failed with exit code {e.returncode}.")
        print("  - STDERR:")
        for line in e.stderr.strip().split("\n"):
            print(f"    {line}")
        raise


def main():
    """Main function to parse arguments and drive the build process."""
    parser = argparse.ArgumentParser(
        description="Unified build script for the project.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--target",
        "-t",
        help="The build target or group to execute.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available build targets and groups.",
    )

    args = parser.parse_args()
    config = load_config()

    if args.list:
        print("--- Available Build Targets ---")
        for name, details in sorted(config["targets"].items()):
            print(f"  - {name}: {details.get('description', 'N/A')}")
        print("\n--- Available Build Groups ---")
        for name, members in sorted(config["build_groups"].items()):
            print(f"  - {name}: (runs {', '.join(members)})")
        return

    if not args.target:
        parser.error("A --target must be specified.")

    target_or_group = args.target
    if target_or_group in config.get("build_groups", {}):
        print(f"--- Executing Build Group: {target_or_group.upper()} ---")
        for target_name in config["build_groups"][target_or_group]:
            execute_build(target_name, config)
        print(f"\n--- Group '{target_or_group}' Finished ---")
    elif target_or_group in config["targets"]:
        execute_build(target_or_group, config)
        print(f"\n--- Target '{target_or_group}' Finished ---")
    else:
        raise ValueError(f"Target or group '{target_or_group}' not found.")


if __name__ == "__main__":
    main()
