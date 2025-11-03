# tooling/lint.py
import subprocess
import sys


def run_command(command):
    """Runs a command and returns its exit code."""
    try:
        subprocess.run(command, check=True, shell=True, text=True, capture_output=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"--- Failure: {command} failed. ---")
        print(f"--- STDOUT ---\n{e.stdout}")
        print(f"--- STDERR ---\n{e.stderr}")
        return e.returncode


def main():
    """Main function to run linting checks."""
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        autoflake_command = "autoflake --in-place --remove-all-unused-imports --recursive ."
        black_command = "black ."
    else:
        autoflake_command = "autoflake --check --remove-all-unused-imports --recursive ."
        black_command = "black --check ."

    pyflakes_command = "pyflakes ."

    print("--- Running Autoflake ---")
    autoflake_exit_code = run_command(autoflake_command)

    print("--- Running Pyflakes ---")
    pyflakes_exit_code = run_command(pyflakes_command)

    print("--- Running Black ---")
    black_exit_code = run_command(black_command)

    if autoflake_exit_code != 0 or pyflakes_exit_code != 0 or black_exit_code != 0:
        print("--- Linting Failed ---")
        sys.exit(1)

    print("--- Linting Passed ---")


if __name__ == "__main__":
    main()
