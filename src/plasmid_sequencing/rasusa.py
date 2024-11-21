## rasusa

def rasusa(input, coverage=200, genome_size='10kb', iterations=3):
    """
    Randomly subsample a FASTQ to a given average coverage.
    
    Parameters:
        input (str): Path to the input fastq.
        coverage (int): Target genome coverage.
        genome_size (str): Target genome size in bases.
        iterations (int): The int number of subsample files to write.

    Returns:
        output_file_list (list of str): List of filepaths of the rasusa subsamples
    """
    import subprocess
    import os

    input_basename = os.path.basename(input)
    split_basename = input_basename.split('.fastq')
    output_file_list = []
    for iteration in range(iterations):
        output_basename = split_basename[0] + '_' + f'rasusa_subsample_{iteration}' + '.fastq.gz'
        output_path = os.path.join(os.path.dirname(input), output_basename)
            
        command_list = ['rasusa', 'reads', input, '-c', coverage, '-g', genome_size]
        random_seed = ['-s', 1]
        output_list = ['-o', output_path]

        command_list += random_seed + output_list

        subprocess.run(command_list)

        output_file_list.append(output_path)

    return output_file_list