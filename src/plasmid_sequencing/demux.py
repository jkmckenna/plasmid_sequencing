## demux

def demux(input_path, barcode_kit='SQK-RBK114-96', split_dir='demultiplexed_fastqs', emit_fastq=True):
    """
    Wrapper function for dorado demultiplexing. Outputs demultiplexed samples into the output directory.

    Parameters:
        input_path (str): Path to the input BAM file
        barcode_kit (str): A string reppresenting the barcoding kit used in the experiment.
        split_dir (str): A string representing the directory name to emit demultiplexed samples into relative to the input path.
        emit_fastq (bool): If True, emits a FASTQ. If False, emits a demultiplexed BAM. The BAM contains more information in it's SAM tags that is lost in the FASTQ.
    
    Returns:
        output_directory (str): String representing the output directory root.
    """
    import os
    import subprocess

    command = ["dorado", "demux", "--kit-name", barcode_kit, '--output-dir', split_dir]

    if emit_fastq:
        command.append('--emit-fastq')

    command.append(input_path)
    command_string = " ".join(command)
    print(f"Running {command_string}\n to generate demultiplexed outputs")

    subprocess.run(command)

    input_directory = os.path.dirname(input_path)
    output_directory = os.path.join(input_directory, split_dir)

    return output_directory