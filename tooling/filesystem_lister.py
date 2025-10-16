import os
import fnmatch


def _get_gitignore_patterns(gitignore_path=".gitignore"):
    """Reads and parses the .gitignore file."""
    if not os.path.exists(gitignore_path):
        return []
    with open(gitignore_path, "r") as f:
        patterns = f.read().splitlines()
    # Filter out empty lines and comments
    return [p for p in patterns if p and not p.startswith("#")]


def list_all_files_and_dirs(root_dir=".", use_gitignore=True):
    """
    Walks through a directory and its subdirectories and returns a sorted list of all
    files and directories.

    Args:
        root_dir (str): The root directory to start the walk from.
        use_gitignore (bool): If True, respects the patterns in the .gitignore file.
    """
    item_list = []
    gitignore_patterns = (
        _get_gitignore_patterns(os.path.join(root_dir, ".gitignore"))
        if use_gitignore
        else []
    )

    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Filter directories in-place to prevent os.walk from traversing them
        if use_gitignore:
            original_dirs = list(dirs)
            dirs[:] = []
            for d in original_dirs:
                dir_path = os.path.join(root, d)
                rel_dir_path = os.path.relpath(dir_path, root_dir) + "/"
                if not any(
                    fnmatch.fnmatch(rel_dir_path, p) for p in gitignore_patterns
                ):
                    dirs.append(d)

        # Add directories to the list
        for d in dirs:
            dir_path = os.path.join(root, d)
            item_list.append(os.path.relpath(dir_path, root_dir) + "/")

        # Add files to the list
        for f in files:
            file_path = os.path.join(root, f)
            rel_file_path = os.path.relpath(file_path, root_dir)
            if use_gitignore:
                if not any(
                    fnmatch.fnmatch(rel_file_path, p) for p in gitignore_patterns
                ):
                    item_list.append(rel_file_path)
            else:
                item_list.append(rel_file_path)

    return sorted(list(set(item_list)))
