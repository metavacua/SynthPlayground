"""
This module provides a centralized and standardized interface for all file
system operations within the agent's environment. It aims to address issues of
inconsistent path handling, duplicated file discovery logic, and ad-hoc
filtering by providing a single, reliable implementation for these common tasks.

Core Features:
- **Standardized Path Construction:** All path manipulations are handled using
  `os.path.join` to ensure cross-platform compatibility.
- **Centralized File Discovery:** A single function for finding files based on
  patterns, with built-in support for a centralized ignore mechanism.
- **Robust Error Handling:** Functions are designed to gracefully handle common
  file system errors, such as permission issues or broken links.
- **Centralized Ignore Mechanism:** File and directory filtering is managed via
  a `.julesignore` file in the repository root, providing a single source of
  truth for exclusion patterns.
"""

import os
import fnmatch
import sys

# --- Constants ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IGNORE_FILE = os.path.join(ROOT_DIR, ".julesignore")


def get_ignore_patterns(base_dir):
    """
    Loads ignore patterns from the .julesignore file in the specified base directory.
    Returns two sets of patterns: one for directories and one for files.
    """
    ignore_file_path = os.path.join(base_dir, ".julesignore")
    dir_patterns = set()
    file_patterns = set()
    if not os.path.exists(ignore_file_path):
        return dir_patterns, file_patterns
    try:
        with open(ignore_file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.endswith("/"):
                    dir_patterns.add(line.rstrip("/"))
                else:
                    file_patterns.add(line)
    except (IOError, OSError) as e:
        print(f"Error reading ignore file: {e}", file=sys.stderr)
    return dir_patterns, file_patterns


def find_files(pattern, base_dir=ROOT_DIR, recursive=True):
    """
    Finds all files matching a given pattern, respecting the .julesignore file.
    Can perform both recursive and non-recursive searches.
    """
    dir_patterns, file_patterns = get_ignore_patterns(base_dir)
    matches = []
    try:
        if recursive:
            for root, dirnames, filenames in os.walk(base_dir, topdown=True):
                # Exclude ignored directories from traversal
                dirnames[:] = [
                    d
                    for d in dirnames
                    if not any(fnmatch.fnmatch(d, p) for p in dir_patterns)
                ]

                for filename in filenames:
                    if any(fnmatch.fnmatch(filename, p) for p in file_patterns):
                        continue
                    if fnmatch.fnmatch(filename, pattern):
                        filepath = os.path.join(root, filename)
                        matches.append(os.path.relpath(filepath, base_dir))
        else:
            # Non-recursive search
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isfile(item_path):
                    if any(fnmatch.fnmatch(item, p) for p in file_patterns):
                        continue
                    if fnmatch.fnmatch(item, pattern):
                        matches.append(item)

    except (IOError, OSError) as e:
        print(f"Error during file search: {e}", file=sys.stderr)
    return matches


def find_protocol_dirs(root_dir):
    """
    Finds all directories within the root_dir that contain at least one
    `.protocol.json` or `.protocol.md` file, indicating they are protocol modules.
    """
    protocol_dirs = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".protocol.json") or filename.endswith(".protocol.md"):
                protocol_dirs.add(dirpath)
                break  # Move to the next directory once one protocol file is found
    return list(protocol_dirs)


def get_protocol_dir_name(dir_path):
    """
    Returns a human-readable name for a protocol directory.
    If it's the root protocols directory, it returns 'root'.
    Otherwise, it returns the directory's base name.
    """
    if os.path.basename(dir_path) == "protocols":
        return "root"
    return os.path.basename(dir_path)
