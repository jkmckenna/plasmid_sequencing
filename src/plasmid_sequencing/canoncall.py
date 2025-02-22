## canoncall

# Conversion SMF specific
def canoncall(pod5_dir, model='/Users/josephmckenna/dorado-0.5.3-osx-arm64/dorado_models/dna_r10.4.1_e8.2_400bps_hac@v4.3.0', barcode_kit='SQK-RBK114-96', bam='output', bam_suffix='.bam'):
    """
    Wrapper function for dorado canonical base calling.

    Parameters:
        pod5_dir (str): a string representing the file path to the experiment directory containing the POD5 files.
        model (str): a string representing the file path to the dorado basecalling model.
        barcode_kit (str): A string reppresenting the barcoding kit used in the experiment.
        bam (str): File path to the BAM file to output.
        bam_suffix (str): The suffix to use for the BAM file.
    
    Returns:
        None
            Outputs a BAM file holding the canonical base calls output by the dorado basecaller.
    """
    import subprocess
    output = bam + bam_suffix
    command = ["dorado", "basecaller", model, pod5_dir, "--kit-name", barcode_kit, "-Y"]
    command_string = " ".join(command)
    print(f"Running {command_string}\n to generate {output}")
    with open(output, "w") as outfile:
        subprocess.run(command, stdout=outfile)