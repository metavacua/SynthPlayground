import os
import json
import argparse

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_FILE_PATH = os.path.join(ROOT_DIR, ".file_index.json")
# Exclude common volatile or uninteresting directories and files
DEFAULT_EXCLUDES = {".git", ".idea", "__pycache__", "node_modules", "target", "build", "dist"}
DEFAULT_EXCLUDE_PATTERNS = {".DS_Store", "*.pyc", "*.swp"}


def get_all_files(root_dir, excludes, exclude_patterns):
    """
    Walks the directory tree and returns a sorted list of all file paths.

    Args:
        root_dir (str): The root directory to start the walk from.
        excludes (set): A set of directory and file names to exclude.
        exclude_patterns (set): A set of file name patterns to exclude.

    Returns:
        list: A sorted list of relative file paths.
    """
    all_files = set()
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Modify dirs in-place to exclude specified directories
        dirs[:] = [d for d in dirs if d not in excludes]

        for name in files:
            # Check against direct excludes and patterns
            if name in excludes or any(name.endswith(p.strip('*')) for p in exclude_patterns):
                continue

            relative_path = os.path.relpath(os.path.join(root, name), root_dir)
            all_files.add(relative_path)

    return sorted(list(all_files))


def build_index(args):
    """
    Scans the repository and builds the file index.
    """
    print("Building file index...")
    excludes = DEFAULT_EXCLUDES.copy()
    if args.exclude:
        excludes.update(args.exclude)

    files = get_all_files(ROOT_DIR, excludes, DEFAULT_EXCLUDE_PATTERNS)

    try:
        with open(INDEX_FILE_PATH, "w") as f:
            json.dump(files, f, indent=2)
        print(f"Successfully built index with {len(files)} files.")
        print(f"Index saved to: {INDEX_FILE_PATH}")
    except IOError as e:
        print(f"Error: Could not write to index file at {INDEX_FILE_PATH}", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the file indexer CLI."""
    parser = argparse.ArgumentParser(
        description="A tool to create and manage a file index for the repository."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available subcommands", required=True
    )

    # --- Build Command ---
    build_parser = subparsers.add_parser(
        "build", help="Builds or rebuilds the file index."
    )
    build_parser.add_argument(
        "--exclude",
        nargs="+",
        help="Additional directories or files to exclude from the index.",
    )
    build_parser.set_defaults(func=build_index)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()