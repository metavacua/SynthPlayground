import os

def list_all_files_and_dirs(root_dir="."):
    """
    Walks through a directory and its subdirectories and returns a sorted list of all
    files and directories, including empty directories.
    """
    item_list = []
    for root, dirs, files in os.walk(root_dir):
        # Add directories
        for d in dirs:
            dir_path = os.path.join(root, d)
            item_list.append(os.path.relpath(dir_path, root_dir) + "/")

        # Add files
        for f in files:
            file_path = os.path.join(root, f)
            item_list.append(os.path.relpath(file_path, root_dir))

    # Add the root directory itself
    item_list.append("./")

    return sorted(list(set(item_list)))