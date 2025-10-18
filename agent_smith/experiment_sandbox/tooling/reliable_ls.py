"""
A tool for reliably listing files and directories.

This script provides a consistent, sorted, and recursive listing of files and
directories, excluding the `.git` directory. It is intended to be a more
reliable alternative to the standard `ls` command for agent use cases.
"""
import os
import sys

def reliable_ls(start_path="."):
    """
    Recursively lists all directories and files under the start_path.

    Args:
        start_path: The directory to start the traversal from.
    """
    if not os.path.isdir(start_path):
        print(f"Error: Starting path '{start_path}' is not a directory or does not exist.")
        return

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Sort directories and files to ensure a consistent order
        dirs.sort()
        files.sort()

        # Modify dirs in-place to exclude .git
        if ".git" in dirs:
            dirs.remove(".git")

        # Print the root directory
        # We add a trailing slash to directories for clarity
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")

        # Print the subdirectories
        sub_indent = " " * 4 * (level + 1)
        for d in dirs:
            print(f"{sub_indent}{d}/")

        # Print the files in the current directory
        for f in files:
            print(f"{sub_indent}{f}")

def main():
    """
    Main function to run the reliable_ls tool from the command line.
    """
    if len(sys.argv) > 2:
        print("Usage: python tooling/reliable_ls.py [path]")
        sys.exit(1)

    path_to_list = sys.argv[1] if len(sys.argv) == 2 else "."
    reliable_ls(path_to_list)

if __name__ == "__main__":
    main()