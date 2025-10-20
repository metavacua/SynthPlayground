"""
A command-line tool for executing APPL files.

This script provides a simple interface to run APPL files using the main
`run.py` interpreter. It captures and prints the output of the execution,
and provides detailed error reporting if the execution fails.
"""

import subprocess
import sys


def run_appl_file(filepath: str) -> str:
    """
    Executes an APPL file using the run.py interpreter.

    Args:
        filepath: The path to the .appl file to execute.

    Returns:
        The output from the APPL interpreter.
    """
    try:
        command = [sys.executable, "run.py", filepath]
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, encoding="utf-8"
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return f"Error: The file '{filepath}' was not found."
    except subprocess.CalledProcessError as e:
        # Enhanced error reporting
        error_output = f"Error executing APPL file: '{filepath}'\n"
        error_output += f"  Return code: {e.returncode}\n"
        error_output += f"  Command: {' '.join(e.cmd)}\n"
        if e.stdout:
            error_output += f"  stdout:\n{e.stdout.strip()}\n"
        if e.stderr:
            error_output += f"  stderr:\n{e.stderr.strip()}\n"
        return error_output
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def main():
    """
    Main function to run the APPL runner from the command line.
    """
    if len(sys.argv) != 2:
        print("Usage: python tooling/appl_runner.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    output = run_appl_file(filepath)
    print(output)


if __name__ == "__main__":
    main()
