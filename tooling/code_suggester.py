"""
Handles the generation and application of autonomous code change suggestions.

This tool is a key component of the advanced self-correction loop. It is
designed to be invoked by the self-correction orchestrator when a lesson
contains a 'propose-code-change' action.

For its initial implementation, this tool acts as a structured executor. It
takes a lesson where the 'details' field contains a fully-formed git-style
merge diff and applies it to the target file. It does this by generating a
temporary, single-step plan file and signaling its location for the master
controller to execute.

This establishes the fundamental workflow for autonomous code modification,
decoupling the suggestion logic from the execution logic. Future iterations
can enhance this tool with more sophisticated code generation capabilities
(e.g., using an LLM to generate the diff from a natural language description)
without altering the core orchestration process.
"""

import argparse
import os
import tempfile


def generate_suggestion_plan(filepath: str, diff_content: str) -> str:
    """
    Generates a temporary, single-step plan file to apply a code change.

    Args:
        filepath: The path to the file that needs to be modified.
        diff_content: The git-style merge diff block to be applied.

    Returns:
        The path to the generated temporary plan file.
    """
    plan_content = f"""\
replace_with_git_merge_diff
{filepath}
{diff_content}
"""
    # Create a temporary file to store the plan
    fd, plan_path = tempfile.mkstemp(suffix=".plan.txt", text=True)
    with os.fdopen(fd, "w") as tmp:
        tmp.write(plan_content)

    return plan_path


def main():
    """
    Main entry point for the code suggester tool.
    Parses arguments, generates a plan, and prints the plan's path to stdout.
    """
    parser = argparse.ArgumentParser(
        description="Generate a plan to apply a code change suggestion."
    )
    parser.add_argument(
        "--filepath", required=True, help="The path to the file to be modified."
    )
    parser.add_argument(
        "--diff", required=True, help="The git-style merge diff content to apply."
    )

    args = parser.parse_args()

    # The diff content might be passed with escaped newlines; un-escape them.
    diff_content = args.diff.replace("\\n", "\n")

    plan_path = generate_suggestion_plan(args.filepath, diff_content)

    # The orchestrator will read this path from stdout to know which plan to execute.
    print(plan_path)


if __name__ == "__main__":
    main()
