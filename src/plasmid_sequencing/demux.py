## demux

def demux(input_path, barcode_kit='SQK-RBK114-96', split_dir='demultiplexed_samples', emit_fastq=True):
    """
    Wrapper function for dorado canonical base calling.

    Parameters:
        barcode_kit (str): A string reppresenting the barcoding kit used in the experiment.
    
    Returns:
        None
            Outputs a BAM file holding the canonical base calls output by the dorado basecaller.
    """
    import subprocess
    command = ["dorado", "demux", "--kit-name", barcode_kit, '--output-dir', split_dir]
    if emit_fastq:
        command.append('--emit-fastq')

    command.append(input_path)
    command_string = " ".join(command)
    print(f"Running {command_string}\n to generate demultiplexed outputs")
    subprocess.run(command)