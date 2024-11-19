## fastcat

def fastcat(input, recurse=True, output_directory='concatenated_fastqs', file_summaries='file_summaries.txt', min_length=1000, max_length=False, min_quality=10):
    """
    Concatenate FASTQSs in an input directory and output the file into a subdirectory named concatenated.
    Besides concatenating, this command thresholds output FASTQ based on read lengths and quality.
    Histograms of read lengths and quality are also output.
    
    Parameters:
        input (str): Path to the input fastq or directory containing fastqs to use.
        recurse (bool): If True, add the -x option to recursively searches all subdirectories for FASTQs. 
        output_directory (bool | str): If False, output everything to the current directory. Otherwise, -d option creates a new directory to contain the concatenated FASTQs for each barcode.
        file_summaries (bool | str): -f option creates a txt file with basic metrics from each file in the analysis.
        min_length (bool | int): -a option is the minimum read length that will be included in the concatenated FASTQ output.
        max_length (bool | int): -b option is the maximum read length that will be included in the concatenated FASTQ output.
        min_quality (bool | int) -q option is the minimum Q-score that will be included in the concatenated FASTQ output.
    """
    import subprocess
    import os

    if os.path.isdir(input):
        input_isdir = True
    elif '.fastq' in os.path.basename(input):
        input_isdir = False
    else:
        return

    command_list = ['fastcat']

    if input_isdir and recurse:
        command_list.append('-x')

    if output_directory:
        output_command_list = ['-d', output_directory]
        command_list.append(output_command_list)
    
    if file_summaries:
        output_command_list = ['-f', file_summaries]
        command_list.append(output_command_list)   

    if min_length:
        output_command_list = ['-a', min_length]
        command_list.append(output_command_list)  

    if max_length:
        output_command_list = ['-b', max_length]
        command_list.append(output_command_list)  

    if min_quality:
        output_command_list = ['-q', min_quality]
        command_list.append(output_command_list)      

    command_list.append(input)           

    subprocess.run(command_list)