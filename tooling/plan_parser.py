"""
Parses a plan file into a structured list of commands.

This module provides the `parse_plan` function and the `Command` dataclass,
which are central to the agent's ability to understand and execute plans.
The parser correctly handles multi-line arguments and ignores comments,
allowing for robust and readable plan files.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Command:
    """
    Represents a single, parsed command from a plan.
    This structure correctly handles multi-line arguments for tools.
    """

    tool_name: str
    args_text: str


def parse_plan(plan_content: str) -> List[Command]:
    """
    Parses the raw text of a plan into a list of Command objects.
    This parser correctly handles multi-line arguments and ignores comments.
    Commands are expected to be separated by one or more blank lines.
    """
    commands = []
    # Split by double newline to handle multi-line arguments correctly
    command_blocks = plan_content.strip().split("\n\n")

    for block in command_blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue

        lines = block.split("\n")
        # Filter out comment lines within a block
        non_comment_lines = [line for line in lines if not line.strip().startswith("#")]

        if not non_comment_lines:
            continue

        tool_name = non_comment_lines[0].strip()
        args_text = "\n".join(non_comment_lines[1:]).strip()

        commands.append(Command(tool_name=tool_name, args_text=args_text))

    return commands