## medaka

def medaka(input, draft, output=0, threads=4):
    """
    Assembly polishing
    
    Parameters:
        input (str): Path to the input fastq.
        draft (str): Path to the draft assembly to polish.
        output (int): An int to append to the medaka consensus output as a suffix.
        threads (int): Number of threads to allocate

    Return:
        output_path (str): Path to the output flye directory
    """
    import subprocess
    import os

    parent_dir = os.path.dirname(draft)
    output_dir_basename = f'medaka_consensus_{output}'
    output_path = os.path.join(parent_dir, output_dir_basename)

    command_list = ['medaka_consensus', '-i', input, '-d', draft, '-o', output_path, '-t', threads]
    command_string = " ".join(command_list)
    print(f'Running: {command_string}')

    subprocess.run(command_list)

def recursive_medaka(input_dir, output_dir):
    """
    Polish the de novo flye assemblies.

    Parameters:
        input_dir (str): Path to the directory containing the trimmed sample FASTQ.
        output_dir (str): Path to root directory of the flye outputs

    Returns:
        None

    """
    import os
    import subprocess

    for sample_id in os.listdir(input_dir):
        sample_dir_a = os.path.join(input_dir, sample_id)
        sample_dir_b = os.path.join(output_dir, sample_id)
        
        # Check if sample directories exist
        if not os.path.isdir(sample_dir_a) or not os.path.isdir(sample_dir_b):
            continue
        
        # Locate the FASTQ file in the input_dir
        fastq_files = [f for f in os.listdir(sample_dir_a) if '.fastq' in f and 'porechop' in f]
        if not fastq_files:
            print(f"No FASTQ file found in {sample_dir_a}")
            continue
        fastq_file = os.path.join(sample_dir_a, fastq_files[0])
        print(f"Found FASTQ file: {fastq_file}")
        
        # Iterate through subdirectories of the output_dir
        for i, sub_dir in enumerate(os.listdir(sample_dir_b)):
            if 'flye' in sub_dir:
                fasta_dir = os.path.join(sample_dir_b, sub_dir)
                if not os.path.isdir(fasta_dir):
                    continue
            
                # Locate the FASTA file in the subdirectory
                fasta_files = [f for f in os.listdir(fasta_dir) if f == 'assembly.fasta']
                if not fasta_files:
                    print(f"No FASTA file found in {fasta_dir}")
                    continue
                fasta_file = os.path.join(fasta_dir, fasta_files[0])
                print(f"Found FASTA file: {fasta_file}")
                
                # Run polishing operation
                try:
                    medaka(fastq_file, fasta_file, output=i)
                except subprocess.CalledProcessError as e:
                    print(f"Error during polishing: {e}")
                    continue