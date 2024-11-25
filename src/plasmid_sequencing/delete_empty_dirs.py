## delete_empty_dirs
import os

def delete_empty_dirs(root_dir):
    """
    Recursively delete empty directories within the specified root directory.

    Parameters:
    - root_dir: Path to the root directory.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Check if the directory is empty (no files or subdirectories)
        if not dirnames and not filenames:
            os.rmdir(dirpath)
            print(f"Deleted empty directory: {dirpath}")