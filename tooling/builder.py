"""
This script provides a unified build interface for the repository.
...
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
import yaml

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_CONFIG_PATH = os.path.join(ROOT_DIR, "build_config.yaml")


def load_build_config():
    """Loads the build configuration from the YAML file."""
    with open(BUILD_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def execute_build(target_name, build_config, extra_args):
    """Executes a single build target."""
    if target_name not in build_config["targets"]:
        raise ValueError(f"Unknown build target: {target_name}")

    target_config = build_config["targets"][target_name]
    target_type = target_config["type"]
    print(f"--- Building Target: {target_name.upper()} ---")
    print(f"  - Type:     {target_type}")
    print(f"  - Desc:     {target_config.get('description', 'N/A')}")
    start_time = time.time()

    if target_type == "compiler":
        from tooling.build_logic import generate_compiler_command
        command, command_str = generate_compiler_command(
            target_config, ROOT_DIR, extra_args
        )
        print(f"  - Command:  {command_str}")
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=ROOT_DIR,
            )
            print("  - Status:   SUCCESS")
            print(f"  - Duration: {time.time() - start_time:.2f}s")
            print(f"  - STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"  - STDERR:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            print("  - Status:   FAILURE")
            print(f"  - Duration: {time.time() - start_time:.2f}s")
            print(f"  - ERROR:    Command failed with exit code {e.returncode}")
            print(f"  - STDOUT:\n{e.stdout}")
            print(f"  - STDERR:\n{e.stderr}")

    elif target_type == "command":
        command = target_config["command"].strip()
        print(f"  - Command:  {command}")
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                shell=True,
                cwd=ROOT_DIR,
            )
            print("  - Status:   SUCCESS")
            print(f"  - Duration: {time.time() - start_time:.2f}s")
            print(f"  - STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"  - STDERR:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            print("  - Status:   FAILURE")
            print(f"  - Duration: {time.time() - start_time:.2f}s")
            print(f"  - ERROR:    Command failed with exit code {e.returncode}")
            print(f"  - STDOUT:\n{e.stdout}")
            print(f"  - STDERR:\n{e.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Unified build script.")
    parser.add_argument(
        "--target",
        required=True,
        help="The build target or group to execute.",
    )
    args, extra_args = parser.parse_known_args()
    build_config = load_build_config()

    if args.target in build_config.get("build_groups", {}):
        print(f"--- Executing Build Group: {args.target.upper()} ---")
        for target in build_config["build_groups"][args.target]:
            execute_build(target, build_config, extra_args)
        print(f"\n--- Group '{args.target}' Finished ---")
    elif args.target in build_config["targets"]:
        execute_build(args.target, build_config, extra_args)
    else:
        print(f"Error: Target '{args.target}' not found in build_config.yaml")
        sys.exit(1)


if __name__ == "__main__":
    main()
