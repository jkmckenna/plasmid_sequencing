## extract_histogram_stats

def extract_histogram_stats(input_path):
    """
    
    Parameters:

    """
    import os
    import numpy as np

    # Root directory containing sample subdirectories
    output_file = os.path.join(input_path, "read_summary_statistics.txt")

    # Initialize a list to hold the results
    summary = []

    # Traverse the directory tree
    for subdir, dirs, files in os.walk(input_path):
        # Check if the current folder is named "histograms"
        if os.path.basename(subdir) == "histograms":
            # Extract the sample name (two levels above)
            sample_name = os.path.basename(os.path.dirname(subdir))
            
            # Process each histogram file in the current "histograms" folder
            for file in files:
                if file.endswith(".txt"):  # Only process .txt files
                    file_path = os.path.join(subdir, file)
                    
                    # Load the histogram data
                    data = np.loadtxt(file_path)
                    start_edges = data[:, 0]
                    end_edges = data[:, 1]
                    counts = data[:, 2]
                    
                    # Calculate the statistics
                    total_counts = np.sum(counts)
                    mean_count = np.mean(counts)
                    median_count = np.median(counts)
                    range_edges = end_edges[-1] - start_edges[0]
                    weighted_mean = np.sum(counts * (start_edges + end_edges) / 2) / total_counts
                    
                    # Append the results as a row to the summary
                    summary.append([
                        sample_name, file, total_counts, mean_count, 
                        median_count, range_edges, weighted_mean
                    ])

    # Sort the summary by sample name (ascending order)
    summary = sorted(summary, key=lambda x: x[0])

    # Write the summary to a file
    with open(output_file, "w") as f:
        # Write the header row
        f.write("Sample\tHistogram File\tTotal Counts\tMean Count\tMedian Count\tRange of Edges\tWeighted Mean\n")
        # Write the data rows
        for row in summary:
            f.write(f"{row[0]}\t{row[1]}\t{row[2]:.2f}\t{row[3]:.2f}\t{row[4]:.2f}\t{row[5]:.2f}\t{row[6]:.2f}\n")
