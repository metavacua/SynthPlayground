"""
This module provides a centralized, robust, and platform-agnostic interface for
all filesystem operations within the agent's toolkit.

It is designed to address the following systemic issues:
- **Inconsistent Path Handling:** All path manipulations are performed using
  `os.path`, ensuring cross-platform compatibility.
- **Lack of Centralized File Discovery:** This module provides a single,
  authoritative source for file and directory discovery.
- **Ad-Hoc Filtering and Ignoring:** A centralized ignore mechanism, similar to
  `.gitignore`, is used to exclude irrelevant files and directories.
- **Insufficient Error Handling:** All traversal logic includes robust error
  handling for common filesystem issues.
"""

import os

# --- Configuration ---

# A list of directories to ignore during file discovery.
IGNORE_DIRS = [".git", "archive", "reports", "postmortems", "logs"]


def find_files(root_dir=".", extensions=None, ignore_dirs=None):
    """
    Recursively finds all files in a directory that match the given extensions,
    excluding specified directories.

    Args:
        root_dir (str): The root directory to start the search from.
        extensions (list, optional): A list of file extensions to include. If
            None, all files are included. Defaults to None.
        ignore_dirs (list, optional): A list of directory names to ignore. If
            None, the default IGNORE_DIRS list is used. Defaults to None.

    Returns:
        list: A list of absolute paths to the found files.
    """
    if ignore_dirs is None:
        ignore_dirs = IGNORE_DIRS

    found_files = []
    try:
        for root, dirs, files in os.walk(os.path.abspath(root_dir), topdown=True):
            # Exclude ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    found_files.append(os.path.join(root, file))
    except OSError as e:
        # In a real application, you'd want to use a proper logger
        print(f"Error during file discovery in '{root_dir}': {e}")

    return found_files