## flye
import subprocess
import os
from pathlib import Path

def flye(input, min_overlap=1000, nano_hq=0.02, nano_raw=False, output='0', output_dir=False):
    """
    De novo genome assembly
    
    Parameters:
        input (str): Path to the input fastq.
        min_overlap (bool | int): --min-overlap specifies the minimum overlap needed between reads.
        nano_hq (bool | float): --nano-hq specifies that the reads are nanopore Q20+ reads. This preceeds the filepath to the input fastq. --read-error specifies proportion of error rate.
        nano_raw (bool): --nano-raw. 
        output (str): -o specifies the output directory suffix.
        output_dir (bool | str): If False, just output subsample into the same directory as the input file. If a string is passed, pass it into that output directory.

    Return:
        output_path (str): Path to the output flye directory
    """

    command_list = ['flye']
    read_error_list = []
    
    if min_overlap:
        command_list += ['--min-overlap', str(min_overlap)]
        
    if nano_hq:
        command_list += ['--nano-hq']
        read_error_list = ['--read-error', str(nano_hq)]
    elif nano_raw:
        command_list += ['--nano-raw']

    parent_dir = os.path.dirname(input)
    output_dir_basename = f'flye_{output}'
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

def recursive_flye(input_dir, output_dir='subsampled_flye_assemblies', min_overlap=1000, nano_hq=0.02, nano_raw=False):
    """
    Recursively search a directory for all fastq files. Produce a de novo assembly for every FASTQ.

    Parameters:
        input_dir (str): Path to the input directory.
        min_overlap (bool | int): --min-overlap specifies the minimum overlap needed between reads.
        nano_hq (bool | float): --nano-hq specifies that the reads are nanopore Q20+ reads. This preceeds the filepath to the input fastq. --read-error specifies proportion of error rate.
        nano_raw (bool): --nano-raw. 
        output (str): -o specifies the output directory suffix.
        output_dir (bool | str): If False, just output subsample into the same directory as the input file. If a string is passed, pass it into that output directory.

    Returns:
        output_dir (str): String representing the root directory that outputs will be stored in.
        output_file_list_of_lists (list of lists): List of lists containing the replicate filepaths for all sample FASTQs.
    """
    input_dir = Path(input_dir)
    parent_dir = input_dir.parent
    output_dir = parent_dir / Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    output_file_list = []

    for root, _, files in os.walk(input_dir):
        rel_path = Path(root).relative_to(input_dir)
        output_subdir = output_dir / rel_path
        output_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file.endswith(".fastq") or file.endswith(".fastq.gz"):
                input_file = Path(root) / file
                flye_iteration = file.split('subsample_')[1]
                flye_iteration = flye_iteration.split('.fastq')[0]
                output_file = flye(input_file, min_overlap, nano_hq, nano_raw, output=flye_iteration, output_dir=output_subdir)
                output_file_list.append(output_file)

    return output_dir, output_file_list