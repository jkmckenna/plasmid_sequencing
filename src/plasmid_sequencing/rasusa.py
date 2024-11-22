## rasusa
from pathlib import Path
import subprocess
import os

def rasusa(input, coverage=200, genome_size='10kb', iterations=3, output_dir=False):
    """
    Randomly subsample a FASTQ to a given average coverage.
    
    Parameters:
        input (str): Path to the input fastq.
        coverage (int): Target genome coverage.
        genome_size (str): Target genome size in bases.
        iterations (int): The int number of subsample files to write.
        output_dir (bool | str): If False, just output subsample into the same directory as the input file. If a string is passed, pass it into that output directory.

    Returns:
        output_file_list (list of str): List of filepaths of the rasusa subsamples
    """

    input_basename = os.path.basename(input)
    split_basename = input_basename.split('.fastq')
    output_file_list = []
    for iteration in range(iterations):
        output_basename = split_basename[0] + '_' + f'rasusa_subsample_{iteration}' + '.fastq.gz'

        if output_dir:
            output_path = os.path.join(output_dir, output_basename)
        else:
            output_path = os.path.join(os.path.dirname(input), output_basename)
            
        command_list = ['rasusa', 'reads', input, '-c', str(coverage), '-g', genome_size]
        random_seed = ['-s', str(1)]
        output_list = ['-o', output_path]

        command_list += random_seed + output_list

        command_string = " ".join(command_list)
        print(f"Running {command_string}")

        subprocess.run(command_list)

        output_file_list.append(output_path)

    return output_file_list

def recursive_rasusa(input_dir, output_dir='subsampled_trimmed_filtered_demuliplexed_fastqs', coverage=200, genome_size='10kb', iterations=3):
    """
    Recursively search a directory for all fastq files. Produce subsamples of a given coverage for each FASTQ.

    Parameters:
        input_dir (str): Path to the input directory.
        coverage (int): Target genome coverage.
        genome_size (str): Target genome size in bases.
        iterations (int): The int number of subsample files to write.
        output_dir (bool | str): If False, just output subsample into the same directory as the input file. If a string is passed, pass it into that output directory.

    Returns:
        output_dir (str): String representing the root directory that outputs will be stored in.
        output_file_list_of_lists (list of lists): List of lists containing the replicate filepaths for all sample FASTQs.
    """
    input_dir = Path(input_dir)
    parent_dir = input_dir.parent
    output_dir = parent_dir / Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    output_file_list_of_lists =[]

    for root, _, files in os.walk(input_dir):
        rel_path = Path(root).relative_to(input_dir)
        output_subdir = output_dir / rel_path
        output_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file.endswith(".fastq") or file.endswith(".fastq.gz"):
                input_file = Path(root) / file

                output_file_list = rasusa(input_file, coverage, genome_size, iterations, output_subdir)
                output_file_list_of_lists.append(output_file_list)

    return output_dir, output_file_list_of_lists
