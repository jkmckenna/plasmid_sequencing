## porechop

def porechop(input, recurse=True, output_suffix='porechopped', extra_end_trim=2, discard_middle=True):
    """
    Trim out adapter and barcode sequences from concatenated fastqs.
    
    Parameters:
        input (str): Path to the input fastq or directory containing fastqs to use.
        recurse (bool): If True, recursively searches all subdirectories for FASTQs. 
        output_suffix (str): String to append to the end of the input basename.
        extra_end_trim (bool | int): How many extra bases to remove adjacent to the adapter.
        discard_middle (bool): Whether to discard reads that have middle adapters

    Return:
        None
    """
    import subprocess
    import os

    if os.path.isdir(input) and recurse:
        fastq_files = []
        for root, _, files in os.walk(input):
            for file in files:
                if file.endswith('.fastq') or file.endswith('.fastq.gz') and 'porechop' not in file:
                    fastq_files.append(os.path.join(root, file))
    elif os.path.isdir(input):
        fastq_files = [file for file in os.listdir(input) if '.fastq' in file]
    elif '.fastq' in os.path.basename(input):
        fastq_files = [input]
    else:
        return
    
    options = []

    if extra_end_trim:
        options += ['--extra_end_trim', str(extra_end_trim)]

    if discard_middle:
        options.append('--discard_middle')

    for fastq in fastq_files:
        input_basename = os.path.basename(fastq)
        split_basename = input_basename.split('.fastq')
        output_basename = split_basename[0] + '_' + output_suffix + '.fastq.gz'
        output_path = os.path.join(os.path.dirname(fastq), output_basename)
        command_list = ['porechop', '-i', fastq, '-o', output_path]
        command_list += options

        subprocess.run(command_list)

    return