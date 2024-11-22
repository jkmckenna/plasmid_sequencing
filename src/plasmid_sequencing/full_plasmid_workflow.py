## full_plasmid_workflow

def full_plasmid_workflow(input_bam):
    """
    De novo genome assembly. Starts from a single basecalled BAM.
    Steps:
    1) Basecalled BAM -> demultiplexed FASTQs.
    2) demultiplexed FASTQs -> filtered, demultiplexed FASTQs (Filtered on read quality and read length metrics).
    3) Filtered, demultiplexed FASTQs -> Trimmed, filtered, demultiplexed FASTQs. (Porechop removal of adapters).
    4) Subsample in triplicate the trimmed, filtered, demultiplexed FASTQs. (Rasusa).
    5) De novo assembly of subsampled replicates for each sample. (Flye).
    6) Generate a consensus assembly from the Flye replicates for each sample. (Trycycler).
    7) Polish the consensus assembly to deal with indels in the assembly.
    8) Align reads to the polished assembly. Generate coverage statistics.
    
    Parameters:
        input_bam (str): Path to the input BAM file.

    """
    from .demux import demux
    from .filter_fastqs import process_directory
    from .porechop import porechop
    from .rasusa import recursive_rasusa
    from .flye import recursive_flye

    # 1) Demultiplex the input BAM file.
    demultiplexed_fastq_dir = demux(input_bam, barcode_kit='SQK-RBK114-96', split_dir='demultiplexed_fastqs', emit_fastq=True)

    # 2) Filter the demultiplexed FASTQs on read quality and read length thresholds.
    demultiplexed_filtered_fastq_dir = process_directory(demultiplexed_fastq_dir, output_dir='filtered_demuliplexed_fastqs', min_length=500, min_mean_quality=12, save_png=True)

    # 3) Porechop the filtered_demultiplexed_fastqs
    porechop(demultiplexed_filtered_fastq_dir, recurse=True, output_suffix='porechopped', extra_end_trim=2, discard_middle=True)

    #4) Rasusa the porechopped files to create subsamples
    rasusa_root_dir, rasusa_sample_file_list = recursive_rasusa(demultiplexed_filtered_fastq_dir, output_dir='subsampled_trimmed_filtered_demuliplexed_fastqs', coverage=200, genome_size='10kb', iterations=3, search_string='porechop')

    #5) For each subsampled FASTQ, produce a de novo assembled scaffold using flye
    flye_root_dir, flye_sample_list = recursive_flye(rasusa_root_dir, min_overlap=1000, nano_hq=False, nano_raw=0.1)




    
