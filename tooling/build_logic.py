"""
This module contains the business logic for the unified build script.
"""

import os

def generate_compiler_command(target_config, root_dir, extra_args):
    """
    Generates the command for a compiler target.
    """
    compiler_path = os.path.join(root_dir, target_config["compiler"])
    source_paths = " ".join([os.path.join(root_dir, s) for s in target_config["sources"]])
    output_path = os.path.join(root_dir, target_config["output"])

    command_template = target_config["command"]

    # Basic placeholder replacement
    command_str = command_template.format(
        compiler=compiler_path,
        source=source_paths,
        output=output_path
    )

    # Add any extra arguments passed to the builder
    if extra_args:
        command_str += " " + " ".join(extra_args)

    command = command_str.split()

    return command, command_str
