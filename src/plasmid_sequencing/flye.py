## flye

def flye(input, min_overlap=1000, nano_hq=False, nano_raw=0.1, output='0'):
    """
    De novo genome assembly
    
    Parameters:
        input (str): Path to the input fastq.
        min_overlap (bool | int): --min-overlap specifies the minimum overlap needed between reads
        nano_hq (bool): --nano-hq specifies that the reads are nanopore Q20+ reads. This preceeds the filepath to the input fastq
        nano_raw (bool | float): --nano-raw if a --read_error value is passed. --read-error specifies proportion of error rate.
        output (str): -o specifies the output directory suffix

    Return:
        output_path (str): Path to the output flye directory
    """
    import subprocess
    import os

    command_list = ['flye']
    read_error_list = []
    
    if min_overlap:
        command_list += ['--min-overlap', min_overlap]
        
    if nano_hq:
        command_list += ['--nano-hq']
    elif nano_raw:
        command_list += ['--nano_raw']
        read_error_list = ['--read-error', nano_raw]

    parent_dir = os.path.pardir(input)
    output_dir_basename = f'flye_{output}'
    output_path = os.path.join(parent_dir, output_dir_basename)
    output_list = ['-o', output_path]

    command_list += [input] + read_error_list + output_list

    subprocess.run(command_list)

    return output_path