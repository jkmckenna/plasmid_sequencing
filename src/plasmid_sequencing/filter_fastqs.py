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

def calculate_median_quality(quality):
    """Calculate the median quality score from a quality string."""
    return statistics.median([ord(char) - 33 for char in quality])

def write_histogram_to_file(data, bin_size, output_path, label, save_png=True):
    """
    Generate and save histogram data to a text file.
    
    Args:
        data (list): List of numerical data (e.g., read lengths or quality scores).
        bin_size (int): Bin size for histogram.
        output_path (Path): Path to the output file.
        label (str): Label for the histogram (e.g., 'Length' or 'Quality').
    """
    from scipy.signal import find_peaks

    min_val = min(data)
    max_val = max(data)
    bins = np.arange(min_val, max_val + bin_size, bin_size)
    histogram, edges = np.histogram(data, bins=bins)

    peaks, _ = find_peaks(histogram, height=2, prominence=2, distance=10)

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
        # Annotate the peaks
        for peak in peaks:
            # Getting the x-coordinate of the peak
            peak_x = (edges[peak] + edges[peak + 1]) / 2
            peak_y = histogram[peak]
            # Annotating the peak on the plot
            plt.annotate(f"Peak: {peak_y}", 
                        xy=(peak_x, peak_y), 
                        xytext=(peak_x + 0.2, peak_y + 1), 
                        arrowprops=dict(facecolor='red', shrink=0.05),
                        fontsize=10, color='red')
        plt.title(f"{label} Distribution")
        plt.grid(axis='y', alpha=0.75)
        plt.tight_layout()
        plt.savefig(png_path)
        plt.close()
        print(f"{label} histogram PNG saved to: {png_path}")

def filter_fastq_and_generate_histograms(input_path, output_path, hist_dir, min_length, min_median_quality, save_png):
    """Filter reads in a FASTQ file and generate histogram data for read lengths and quality."""
    read_lengths = []
    quality_scores = []

    with open(output_path, "w") as out_fq:
        for header, sequence, separator, quality in parse_fastq(input_path):
            read_length = len(sequence)
            median_quality = calculate_median_quality(quality)

            # Collect metrics for histogram
            read_lengths.append(read_length)
            quality_scores.append(median_quality)

            # Apply filters
            if read_length >= min_length and median_quality >= min_median_quality:
                out_fq.write(f"{header}\n{sequence}\n{separator}\n{quality}\n")

    # Write histogram data to text files
    write_histogram_to_file(read_lengths, 1, hist_dir, "Read Length", save_png)
    write_histogram_to_file(quality_scores, 1, hist_dir, "Quality Score", save_png)

def process_directory(input_dir, output_dir='filtered_fastqs', min_length=500, min_median_quality=12, save_png=True):
    """Recursively iterate over FASTQ files in a directory and process them."""
    input_dir = Path(input_dir)
    output_dir = input_dir / Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    for root, _, files in os.walk(input_dir):
        rel_path = Path(root).relative_to(input_dir)
        output_subdir = output_dir / rel_path
        output_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file.endswith(".fastq"):
                input_file = Path(root) / file
                output_file = output_subdir / file
                hist_dir = output_subdir / "histograms"
                hist_dir.mkdir(exist_ok=True)

                print(f"Processing: {input_file} -> {output_file}")
                filter_fastq_and_generate_histograms(input_file, output_file, hist_dir, min_length, min_median_quality, save_png)
