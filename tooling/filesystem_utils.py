"""
A centralized, robust utility for all filesystem operations.
"""
import os
import fnmatch
import pathspec

DEFAULT_IGNORE_PATTERNS = [
    ".git/", ".github/", "*.pyc", "__pycache__/", "*.log", "logs/", "archive/", ".DS_Store"
]

def find_files(
    start_dir=".",
    search_patterns=None,
    ignore_patterns=None,
    ignore_file_path=None,
    recursive=True,
):
    """
    Finds files recursively from a start directory, with powerful filtering using pathspec.
    """
    # Combine all ignore patterns
    final_ignore_patterns = set(DEFAULT_IGNORE_PATTERNS)
    if ignore_file_path and os.path.exists(ignore_file_path):
        final_ignore_patterns.add(os.path.basename(ignore_file_path)) # Ignore the ignore file itself
        with open(ignore_file_path, 'r') as f:
            final_ignore_patterns.update(line.strip() for line in f if line.strip() and not line.startswith('#'))
    if ignore_patterns:
        final_ignore_patterns.update(ignore_patterns)

    spec = pathspec.PathSpec.from_lines('gitwildmatch', final_ignore_patterns)

    found_files = []

    for root, dirs, files in os.walk(start_dir, topdown=True):
        # Use relative paths for pathspec matching
        relative_root = os.path.relpath(root, start_dir)
        if relative_root == '.':
            relative_root = ''

        all_paths_relative = [os.path.join(relative_root, name) for name in dirs + files]

        # Filter ignored paths
        ignored_paths_relative = set(spec.match_files(all_paths_relative))

        # Prune directories
        dirs[:] = [d for d in dirs if os.path.join(relative_root, d) not in ignored_paths_relative]

        for name in files:
            file_rel_path = os.path.join(relative_root, name)
            if file_rel_path not in ignored_paths_relative:
                if search_patterns:
                    if any(fnmatch.fnmatch(name, pattern) for pattern in search_patterns):
                        found_files.append(os.path.abspath(os.path.join(root, name)))
                else:
                    found_files.append(os.path.abspath(os.path.join(root, name)))

        if not recursive:
            break

    return sorted(list(set(found_files)))