## nest_file

def nest_file(input_dir, prefix_to_remove='SQK-RBK114-96_', file_extension='.fastq'):
    """
    Take all files within a directory and nest them within their own respective subdirectory.

    Parameters:    

    """
    import os
    import shutil

    # List all FASTQ files in the directory
    files = os.listdir(input_dir)
    files = [file for file in files if file.endswith(file_extension)]
    for file_name in files:
        # Get the file name without the extension
        folder_name = os.path.splitext(file_name)[0]
        try:
            folder_name = folder_name.split(prefix_to_remove)[1]
        except:
            pass
        
        folder_path = os.path.join(input_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Move the file into the new folder
        source_path = os.path.join(input_dir, file_name)
        destination_path = os.path.join(folder_path, file_name)
        shutil.move(source_path, destination_path)

        print(f"Moved {file_name} to {folder_path}")