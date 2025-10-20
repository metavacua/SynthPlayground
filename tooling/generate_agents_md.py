import argparse


def generate_executable_agents_md(source_file, output_file):
    """
    Generates a self-executing AGENTS.md file by embedding the markdown
    content into a Python script's docstring.
    """
    with open(source_file, "r") as f:
        markdown_content = f.read()

    # Escape triple quotes in the markdown content to avoid breaking the python string
    markdown_content_escaped = markdown_content.replace('"""', '"""')

    script_to_embed = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{markdown_content_escaped}
"""

import re
import subprocess

def main():
    """
    This script is a self-executing Markdown file.
    It parses its own content to find and execute shell commands.
    """
    # Use the __doc__ attribute to get the docstring, which is the Markdown content.
    markdown_content = __doc__

    commands = re.findall(r'```bash\\n(.*?)\\n```', markdown_content, re.DOTALL)

    for command in commands:
        # Replace the $(BUILDER) variable with the actual builder command.
        command = command.replace("$(BUILDER)", "python3 tooling/builder.py")
        print(f"--- Executing: {{command.strip()}} ---")
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"--- Command failed with exit code {{e.returncode}} ---")
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
        print("--- Done ---")

if __name__ == "__main__":
    main()
'''
    with open(output_file, "w") as f:
        f.write(script_to_embed)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-executing AGENTS.md file from a template."
    )
    parser.add_argument(
        "--source-file",
        required=True,
        help="The path to the source AGENTS.standard.md file.",
    )
    parser.add_argument(
        "--output-file", required=True, help="The path to the output AGENTS.md file."
    )
    args = parser.parse_args()

    generate_executable_agents_md(args.source_file, args.output_file)
    print(f"Successfully generated {{args.output_file}} from {{args.source_file}}")


if __name__ == "__main__":
    main()
