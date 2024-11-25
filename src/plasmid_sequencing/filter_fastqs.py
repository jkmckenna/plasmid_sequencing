## filter_fastqs

import os
from pathlib import Path
import statistics
import numpy as np
import matplotlib.pyplot as plt

def parse_fastq(file_path):
    """Generator to parse a FASTQ file and yield read tuples."""
    with open(file_path, "r") as fq:
        while True:
            header = fq.readline().strip()
            if not header:
                break  # End of file
            sequence = fq.readline().strip()
            separator = fq.readline().strip()
            quality = fq.readline().strip()
            yield header, sequence, separator, quality

def calculate_median_quality(quality_string):
    """Calculate the median quality score from a quality string."""
    return statistics.median([ord(char) - 33 for char in quality_string])

def calculate_mean_quality(quality_string):
    """
    Calculate the mean quality score from a quality score string.
    """
    # Decode ASCII characters to Phred Q scores
    q_scores = [ord(char) - 33 for char in quality_string]
    
    # Calculate and return the mean
    return sum(q_scores) / len(q_scores) if q_scores else 0.0

def write_histogram_to_file(data, bin_size, output_path, label, filter_threshold, n_passed, save_png=True):
    """
    Generate and save histogram data to a text file.
    
    Params:
        data (list): List of numerical data (e.g., read lengths or quality scores).
        bin_size (int): Bin size for histogram.
        output_path (Path): Path to the output file.
        label (str): Label for the histogram (e.g., 'Length' or 'Quality').
        filter_threshold (float): Threshold for read filtering on a given data metric
        n_passed (int): Number of reads passing the current QC metric

    Returns:
        estimated_construct_length (int): Estimated construct length based on read length peak calling
    """
    from scipy.signal import find_peaks

    min_val = min(data)
    max_val = max(data)
    n_data = len(data)
    range_vals = max_val - min_val
    bins = np.arange(min_val, max_val + bin_size, bin_size)
    histogram, edges = np.histogram(data, bins=bins)
    threshold = max(histogram)/2
    mean_annotation_y = threshold * 1.8
    distance_threshold = range_vals // 20
    peaks, _ = find_peaks(histogram, height=threshold, prominence=threshold, distance=distance_threshold)

    estimated_construct_length = (edges[peaks[-1]] + edges[peaks[-1] + 1]) / 2 # Use the peak calling to get the largest read length peak. If the sample is not over-tagmented in the library-prep, this is likely the plasmid size

    txt_path = output_path / f"{label.lower().replace(' ', '_')}s.txt"

    with open(txt_path, "w") as hist_file:
        for i in range(len(histogram)):
            start = round(edges[i], 1)
            end = round(edges[i + 1], 1)
            count = histogram[i]
            if count > 0:
                if type(bin_size) == int:
                    hist_file.write(f"{int(start)}\t{int(end)}\t{count}\n")
                elif type(bin_size) == float:
                    hist_file.write(f"{start:1f}\t{end:1f}\t{count}\n")
    print(f"{label} histogram saved to: {txt_path}")

    # Optionally save histogram as PNG
    if save_png:
        png_path = output_path / f"{label.lower().replace(' ', '_')}_histogram.png"
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=bins, color="blue", edgecolor="black", alpha=0.7)
        plt.xlabel(label)
        plt.ylabel("Frequency")

        # Plot a vertical line for the filter_threshold
        plt.axvline(filter_threshold, color='green', linestyle='solid', linewidth=1)
        
        # Annotate the threshold on the plot
        plt.text(filter_threshold + 0.1, mean_annotation_y, 
                f'Threshold: {filter_threshold:.1f}', color='green', fontsize=10)

        mean_val = np.mean(data)
        # Plot a vertical line for the mean
        plt.axvline(mean_val, color='purple', linestyle='dashed', linewidth=0.5)
        
        # Annotate the mean on the plot
        plt.text(mean_val + 0.1, mean_annotation_y, 
                f'Mean: {mean_val:.1f}', color='purple', fontsize=10)
    
        # Annotate the peaks
        for peak in peaks:
            # Getting the x-coordinate of the peak (midpoint of the bin)
            peak_x = (edges[peak] + edges[peak + 1]) / 2
            peak_y = histogram[peak]
            
            # Annotating the peak on the plot (vertical dashed line)
            plt.axvline(x=peak_x, color='red', linestyle='--', linewidth=0.5)
            plt.annotate(f"Peak: {peak_x:.1f}", 
                        xy=(peak_x, peak_y), 
                        xytext=(peak_x + 0.2, peak_y + 0.05),  # Adjust annotation position
                        fontsize=10, color='red')
        plt.title(f"{label} Distribution from {n_data} total unfiltered reads: {n_passed} reads above threshold")
        plt.grid(axis='y', alpha=0.75)
        plt.tight_layout()
        plt.savefig(png_path)
        plt.close()
        print(f"{label} histogram PNG saved to: {png_path}")
    
    return estimated_construct_length

def filter_fastq_and_generate_histograms(input_path, output_path, hist_dir, min_length, min_mean_quality, save_png):
    """
    Filter reads in a FASTQ file and generate histogram data for read lengths and quality.

    Returns:
        estimated_construct_length (int): Estimated construct length based on peak calling of read lengths
    """
    read_lengths = []
    quality_scores = []
    n_passed_length_threshold = 0
    n_passed_quality_threshold = 0

    with open(output_path, "w") as out_fq:
        for header, sequence, separator, quality in parse_fastq(input_path):
            read_length = len(sequence)
            mean_quality = calculate_mean_quality(quality)

            # Collect metrics for histogram
            read_lengths.append(read_length)
            quality_scores.append(mean_quality)

            if read_length >= min_length:
                n_passed_length_threshold += 1
            if mean_quality >= min_mean_quality:
                n_passed_quality_threshold += 1

            # Apply filters
            if read_length >= min_length and mean_quality >= min_mean_quality:
                out_fq.write(f"{header}\n{sequence}\n{separator}\n{quality}\n")

    # Write histogram data to text files
    estimated_construct_length = write_histogram_to_file(read_lengths, 1, hist_dir, "Read Length", min_length, n_passed_length_threshold, save_png)
    best_quality_mode = write_histogram_to_file(quality_scores, 1, hist_dir, "Quality Score", min_mean_quality, n_passed_quality_threshold, save_png)

    return estimated_construct_length

def process_directory(input_dir, output_dir='filtered_demuliplexed_fastqs', min_length=500, min_mean_quality=12, save_png=True):
    """
    Recursively iterate over FASTQ files in a directory and process them.
    
    Return:
        output_dir
        sample_fastq_to_read_length_mapping (dict): For each processed FASTQ, maps the estimated construct size from that FASTQ.
    """
    from .gzip_fastqs import gzip_fastqs
    from .extract_histogram_stats import extract_histogram_stats


    input_dir = Path(input_dir)
    parent_dir = input_dir.parent
    output_dir = parent_dir / Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    sample_fastq_to_read_length_mapping = {}

    for root, _, files in os.walk(input_dir):
        rel_path = Path(root).relative_to(input_dir)
        output_subdir = output_dir / rel_path
        output_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file.endswith(".fastq"):
                input_file = Path(root) / file
                input_base_minus_suffix = file.split('.fastq')[0]
                new_basename = input_base_minus_suffix + '_filtered.fastq'
                output_file = output_subdir / new_basename
                hist_dir = output_subdir / "histograms"
                hist_dir.mkdir(exist_ok=True)

                print(f"Processing: {input_file} -> {output_file}")
                estimated_construct_length = filter_fastq_and_generate_histograms(input_file, output_file, hist_dir, min_length, min_mean_quality, save_png)
                sample_fastq_to_read_length_mapping[output_file] = estimated_construct_length

    extract_histogram_stats(output_dir)
    gzip_fastqs(output_dir)

    return output_dir, sample_fastq_to_read_length_mapping
