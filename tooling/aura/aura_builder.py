# tooling/aura/aura_builder.py

import os
import argparse
import subprocess
from datetime import datetime
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tooling.build_logic import (
    load_config,
    generate_command,
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_FILE = os.path.join(ROOT_DIR, "aura_build_config.yaml")

def execute_build(target_name, config):
    if target_name not in config["targets"]:
        raise ValueError(f"Target '{target_name}' not found in build configuration.")

    target_config = config["targets"][target_name]
    target_type = target_config.get("type", "command")

    print(f"--- Building Target: {target_name.upper()} ---")

    command, command_str = generate_command(target_name, target_config)

    print(f"  - Command:  {command_str}")

    try:
        subprocess.run(
            command_str,
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            shell=True,
        )
        print("  - Status:   SUCCESS")
    except subprocess.CalledProcessError as e:
        print("  - Status:   FAILURE")
        print(f"  - Error:    Build failed with exit code {e.returncode}.")
        print("  - STDERR:")
        for line in e.stderr.strip().split("\n"):
            print(f"    {line}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Aura build script.")
    parser.add_argument("--target", "-t", help="The build target to execute.")
    args = parser.parse_args()
    config = load_config(CONFIG_FILE)

    if args.target:
        execute_build(args.target, config)
    else:
        parser.error("A --target must be specified.")

if __name__ == "__main__":
    main()
