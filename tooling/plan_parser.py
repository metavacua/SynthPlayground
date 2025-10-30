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
    This parser correctly handles multi-line arguments, comments, and the '---' separator.
    """
    commands = []
    # Split the plan into logical command blocks using '---'
    plan_blocks = plan_content.strip().split("\n---\n")

    for block in plan_blocks:
        block = block.strip()
        if not block:
            continue

        # Split the block into lines and filter out comments
        lines = [line for line in block.split("\n") if not line.strip().startswith("#")]

        if not lines:
            continue

        # The first non-comment line is the tool name and potentially arguments
        first_line = lines[0].strip()
        if first_line == "set_plan":
            tool_name = "set_plan"
            args_text = "\n".join(lines[1:]).strip()
        else:
            parts = first_line.split(":", 1)
            tool_name = parts[0]
            args_text = ""

            if len(parts) > 1:
                args_text = parts[1].strip()

            if not tool_name:
                continue

            # The rest of the lines are also arguments
            if len(lines) > 1:
                if args_text:
                    args_text += "\n"
                args_text += "\n".join(lines[1:]).strip()

        commands.append(Command(tool_name=tool_name, args_text=args_text))

    return commands
