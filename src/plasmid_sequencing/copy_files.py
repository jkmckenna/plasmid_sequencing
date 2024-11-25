## copy_files
import shutil
import os

def copy_files(src_root, dst_root, file_list=["assembly.fasta", "assembly_info.txt"]):
    """
    Copies the directory structure and specific files from the source directory
    to the destination directory.
    
    Parameters:
    - src_root: Path to the root source directory.
    - dst_root: Path to the root destination directory.
    """
    for root, dirs, files in os.walk(src_root):
        # Determine relative path from the source root
        relative_path = os.path.relpath(root, src_root)
        
        # Determine corresponding destination directory
        dst_dir = os.path.join(dst_root, relative_path)
        
        # Ensure the destination directory exists
        os.makedirs(dst_dir, exist_ok=True)
        
        # Copy only the required files
        for file in files:
            if file in file_list:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)
                shutil.copy2(src_file, dst_file)
                print(f"Copied: {src_file} -> {dst_file}")