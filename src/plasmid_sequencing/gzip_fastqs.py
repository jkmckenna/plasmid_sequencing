## gzip_fastqs

def gzip_fastqs(root_dir, delete_unzipped=True):
    """
    Gzip all FASTQ files within the specified directory and its subdirectories.
    
    param 
        root_dir: The root directory to start searching for FASTQ files.
    """
    import os
    import shutil
    import gzip
    # Walk through the directory recursively
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Process only .fastq files
            if filename.endswith('.fastq'):
                file_path = os.path.join(dirpath, filename)
                gzipped_file_path = file_path + '.gz'
                
                # Open the original FASTQ file and the gzipped file
                with open(file_path, 'rb') as f_in:
                    with gzip.open(gzipped_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Optionally, delete the original FASTQ file after gzipping
                if delete_unzipped:
                    os.remove(file_path)
                
                print(f"Compressed: {file_path} -> {gzipped_file_path}")