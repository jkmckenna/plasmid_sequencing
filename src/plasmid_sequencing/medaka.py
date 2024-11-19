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

    parent_dir = os.path.pardir(draft)
    output_dir_basename = f'medaka_consensus_{output}'
    output_path = os.path.join(parent_dir, output_dir_basename)

    command_list = ['medaka_consensus', '-i', input, '-d', draft, '-o', output_path, '-t', threads]

    subprocess.run(command_list)