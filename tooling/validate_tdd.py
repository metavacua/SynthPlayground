import subprocess
import sys
import os

def get_staged_files():
    """Returns a dictionary of staged files and their status."""
    try:
        output = subprocess.check_output(['git', 'diff', '--cached', '--name-status']).decode('utf-8')
    except subprocess.CalledProcessError:
        return {}

    files = {}
    for line in output.splitlines():
        parts = line.split('\t')
        status = parts[0]
        filepath = parts[1]
        files[filepath] = status
    return files

def is_source_file(filepath):
    """
    Checks if a file is a source file that should be covered by TDD.
    """
    return (
        filepath.endswith('.py') and
        not filepath.startswith('tests/') and
        'validate_tdd.py' not in filepath
    )

def find_corresponding_test_file(source_filepath, all_files):
    """
    Finds the corresponding test file for a source file.
    """
    filename = os.path.basename(source_filepath)
    test_filename = f"test_{filename}"

    for file in all_files:
        if file.startswith('tests/') and file.endswith(test_filename):
            return file
    return None

def main():
    staged_files = get_staged_files()
    all_repo_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            all_repo_files.append(os.path.join(root, file).lstrip('./'))


    errors = []
    warnings = []

    for filepath, status in staged_files.items():
        if is_source_file(filepath):
            test_filepath = find_corresponding_test_file(filepath, all_repo_files)

            if status == 'A':  # Added file
                if not test_filepath:
                    errors.append(
                        f"ERROR: New source file '{filepath}' added without a corresponding test file."
                    )
                elif test_filepath not in staged_files:
                    errors.append(
                        f"ERROR: New source file '{filepath}' added, but the corresponding test file '{test_filepath}' is not staged."
                    )
                elif staged_files.get(test_filepath) != 'A':
                    errors.append(
                        f"ERROR: New source file '{filepath}' added, but the corresponding test file '{test_filepath}' was not added in the same commit."
                    )
            elif status == 'M':  # Modified file
                if not test_filepath:
                    warnings.append(
                        f"WARNING: Source file '{filepath}' was modified, but no corresponding test file was found."
                    )
                elif test_filepath not in staged_files:
                    warnings.append(
                        f"WARNING: Source file '{filepath}' was modified, but the corresponding test file '{test_filepath}' was not."
                    )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)

    if warnings:
        for warning in warnings:
            print(warning, file=sys.stderr)

    print("TDD validation successful.")
    sys.exit(0)

if __name__ == '__main__':
    main()
