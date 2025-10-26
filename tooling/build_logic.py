import os
import json
import yaml


def load_config(config_path):
    """Loads the build configuration file (JSON or YAML)."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Build config file not found: {config_path}")

    _, ext = os.path.splitext(config_path)
    with open(config_path, "r") as f:
        if ext in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif ext == ".json":
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {ext}")


def generate_compiler_command(target_name, target_config, root_dir):
    """Generates the command for a 'compiler' type build target."""
    compiler_path = os.path.join(root_dir, target_config["compiler"])
    command = ["python3", compiler_path]

    # Handle sources
    if "sources" in target_config:
        for source in target_config["sources"]:
            # Check if it's a directory or a file
            if source.endswith("/"):
                command.extend(["--source-dir", os.path.join(root_dir, source)])
            else:
                command.extend(["--source-file", os.path.join(root_dir, source)])

    # Handle output
    if "output" in target_config:
        output_path = os.path.join(root_dir, target_config["output"])
        command.extend(["--output-file", output_path])

    # Handle options
    if "options" in target_config:
        for option, value in target_config["options"].items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and ("file" in option or "dir" in option):
                        command.extend([option, os.path.join(root_dir, item)])
                    else:
                        command.extend([option, str(item)])
            else:
                if isinstance(value, str) and ("file" in option or "dir" in option):
                    command.extend([option, os.path.join(root_dir, value)])
                else:
                    command.extend([option, str(value)])

    return command, " ".join(command)


def generate_command(target_name, target_config):
    """Generates the command for a 'command' type build target."""
    command_str = target_config["command"]
    return command_str, command_str
