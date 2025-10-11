import os
import sys


def main():
    """
    Validates the presence and correct naming of the AGENTS.md file in the root directory.

    This script enforces the following rules:
    1. A single file named exactly `AGENTS.md` must exist in the repository root.
    2. If a file with a similar but incorrect name (case-insensitive) is found
       (e.g., `Agent.md`), it's an error.
    3. If no file matching `AGENTS.md` (case-insensitively) is found, it's an error.
    4. If multiple files matching `AGENTS.md` (case-insensitively) are found,
       it's an error.

    Exits with status 0 on success, 1 on failure.
    """
    root_dir = "."
    expected_filename = "AGENTS.md"

    try:
        all_files = os.listdir(root_dir)
    except OSError as e:
        print(
            f"Error: Could not list files in the root directory: {e}", file=sys.stderr
        )
        sys.exit(1)

    found_files = [f for f in all_files if f.lower() == expected_filename.lower()]

    if not found_files:
        print("Error: Protocol file not found.", file=sys.stderr)
        print(
            f"A file named '{expected_filename}' must exist in the root directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(found_files) > 1:
        print("Error: Multiple protocol files found.", file=sys.stderr)
        print(f"Found: {', '.join(found_files)}", file=sys.stderr)
        print(
            f"Please ensure only one file named '{expected_filename}' exists.",
            file=sys.stderr,
        )
        sys.exit(1)

    actual_filename = found_files[0]
    if actual_filename != expected_filename:
        print("Error: Protocol file has incorrect casing.", file=sys.stderr)
        print(
            f"Found '{actual_filename}', but expected '{expected_filename}'.",
            file=sys.stderr,
        )
        print(f"Please rename the file to '{expected_filename}'.", file=sys.stderr)
        sys.exit(1)

    print("Success: Protocol file 'AGENTS.md' is correctly named and present.")
    sys.exit(0)


if __name__ == "__main__":
    main()
