"""
Parses a plan file into a structured list of commands.

This module provides the `parse_plan` function and the `Command` dataclass,
which are central to the agent's ability to understand and execute plans.
The parser correctly handles multi-line arguments and ignores comments,
allowing for robust and readable plan files.
"""
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Command:
    """
    Represents a single, parsed command from a plan.
    This structure correctly handles multi-line arguments for tools.
    """

    tool_name: str
    # The full, multi-line string of arguments for the tool
    args_text: str


def parse_plan(plan_content: str) -> List[Command]:
    """
    Parses the raw text of a plan into a list of Command objects.
    This parser correctly handles multi-line arguments and ignores comments.
    Commands are expected to be separated by one or more blank lines.
    """
    commands = []
    # Split the plan by blank lines to separate command blocks.
    command_blocks = re.split(r'\n\s*\n', plan_content.strip())

    for block in command_blocks:
        if not block.strip():
            continue

        # Filter out comment lines (those starting with '#')
        lines = [
            line for line in block.strip().split('\n') if not line.strip().startswith('#')
        ]

        if not lines:
            continue

        # The first non-comment line contains the tool name and potentially the first line of args
        first_line_parts = lines[0].strip().split(maxsplit=1)
        tool_name = first_line_parts[0]

        # The rest of the first line and all subsequent lines form the arguments
        args_lines = []
        if len(first_line_parts) > 1:
            args_lines.append(first_line_parts[1])
        args_lines.extend(lines[1:])

        args_text = '\n'.join(args_lines).strip()

        commands.append(Command(tool_name=tool_name, args_text=args_text))

    return commands