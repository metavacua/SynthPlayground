import sys


def generate_appl_command(filepath: str) -> list[str]:
    """
    Generates the command to execute an APPL file.

    Args:
        filepath: The path to the .appl file to execute.

    Returns:
        A list of strings representing the command to be executed.
    """
    return [sys.executable, "run.py", filepath]
