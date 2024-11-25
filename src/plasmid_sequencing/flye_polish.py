## flye
import subprocess
import os
from pathlib import Path

def flye_polish(input, draft, nano_hq=0.02, nano_raw=False, output='0', output_dir=False):
    """
    De novo genome assembly
    
    Parameters:
        input (str): Path to the input fastq.
        draft (str): Path to the draft assembly
        nano_hq (bool | float): --nano-hq specifies that the reads are nanopore Q20+ reads. This preceeds the filepath to the input fastq. --read-error specifies proportion of error rate.
        nano_raw (bool): --nano-raw. 
        output (str): -o specifies the output directory suffix.
        output_dir (bool | str): If False, just output subsample into the same directory as the input file. If a string is passed, pass it into that output directory.

    Return:
        output_path (str): Path to the output flye directory
    """

    command_list = ['flye', '--polish-target', draft]
    read_error_list = []
        
    if nano_hq:
        command_list += ['--nano-hq']
        read_error_list = ['--read-error', str(nano_hq)]
    elif nano_raw:
        command_list += ['--nano-raw']

    parent_dir = os.path.dirname(draft)
    output_dir_basename = f'flye_{output}_polished'
    if output_dir:
        output_path = os.path.join(output_dir, output_dir_basename)
    else:
        output_path = os.path.join(parent_dir, output_dir_basename)
    output_list = ['-o', output_path]

    command_list += [str(input)] + read_error_list + output_list

    command_string = " ".join(command_list)
    print(f"Running {command_string}")

    subprocess.run(command_list)

    return output_path

def recursive_flye_polish(input_dir, output_dir):
    """
    Recursively search a directory for all assemblies. Polish all assemblies

    Parameters:
        input_dir (str): Path to the directory containing the trimmed sample FASTQ.
        output_dir (str): Path to root directory of the flye outputs

    Returns:
        None
    """
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
        for sub_dir in os.listdir(sample_dir_b):
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

                i = sub_dir.split('_')[1]
                
                # Run polishing operation
                try:
                    flye_polish(fastq_file, fasta_file, output=i)
                except subprocess.CalledProcessError as e:
                    print(f"Error during polishing: {e}")
                    continue