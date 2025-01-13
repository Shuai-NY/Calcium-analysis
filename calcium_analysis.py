import pandas as pd
import numpy as np
from scipy.signal import find_peaks, peak_widths
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_data(data, time_column, fluorescence_columns):
    # Rescale time to 20 minutes (1200 seconds)
    time = data[time_column] * (1200 / data[time_column].max())
    fluorescence_data = data[fluorescence_columns]

    # Baseline correction (Delta F/F)
    baseline_corrected_data = (fluorescence_data - fluorescence_data.min()) / fluorescence_data.min()

    # Apply Savitzky-Golay smoothing
    smoothed_data = baseline_corrected_data.apply(lambda x: savgol_filter(x, window_length=11, polyorder=3), axis=0)

    return time, smoothed_data

def detect_peaks(time, smoothed_data, prominence=0.05, height=0.05, distance=5):
    peak_details = []

    for column in smoothed_data.columns:
        # Detect peaks
        peaks, properties = find_peaks(
            smoothed_data[column], prominence=prominence, height=height, distance=distance
        )

        # Calculate widths at half-height
        widths, _, left_ips, right_ips = peak_widths(smoothed_data[column], peaks, rel_height=0.5)

        # Frequency and period
        intervals = np.diff(time.iloc[peaks]) if len(peaks) > 1 else []
        period = intervals.mean() if len(intervals) > 0 else np.nan
        frequency = len(peaks) / (1200 / 60)  # Peaks per minute over 20 minutes

        # Add peak details for this region
        for i, peak_idx in enumerate(peaks):
            peak_details.append({
                "Region": column,
                "Time": time.iloc[peak_idx],
                "Amplitude": properties["peak_heights"][i],
                "Width": widths[i] if len(widths) > i else np.nan,
                "Frequency": frequency,
                "Period": period
            })

    return pd.DataFrame(peak_details)

def aggregate_peak_statistics(peak_details):
    aggregated_stats = {
        "Region": [],
        "Total_Peaks": [],
        "Mean_Amplitude": [],
        "Mean_Width": [],
        "Frequency": [],
        "Mean_Period": []
    }

    grouped = peak_details.groupby("Region")

    for region, group in grouped:
        aggregated_stats["Region"].append(region)
        aggregated_stats["Total_Peaks"].append(len(group))
        aggregated_stats["Mean_Amplitude"].append(group["Amplitude"].mean())
        aggregated_stats["Mean_Width"].append(group["Width"].mean())
        aggregated_stats["Frequency"].append(group["Frequency"].iloc[0])  # Same for all peaks in a region
        aggregated_stats["Mean_Period"].append(group["Period"].mean())

    return pd.DataFrame(aggregated_stats)

def save_results(peak_details, aggregated_stats, output_dir):
    peak_details_path = f"{output_dir}/Step2_3_Peak_Characteristics_Scaled.csv"
    aggregated_stats_path = f"{output_dir}/Aggregated_Peak_Statistics_Scaled.csv"

    peak_details.to_csv(peak_details_path, index=False)
    aggregated_stats.to_csv(aggregated_stats_path, index=False)

    return peak_details_path, aggregated_stats_path

def plot_heatmap(smoothed_data, time, output_dir):
    # Z-score normalization
    z_score_data = (smoothed_data - smoothed_data.mean()) / smoothed_data.std()

    # Plot heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(z_score_data.T, cmap="inferno", cbar=True)
    plt.title('Heatmap of Z-Score Normalized Data (Inferno Colormap)')
    plt.xlabel('Time (s)')
    plt.ylabel('Regions/Samples')

    heatmap_png_path = f"{output_dir}/Z_Score_Heatmap_Inferno.png"
    heatmap_pdf_path = f"{output_dir}/Z_Score_Heatmap_Inferno.pdf"
    plt.savefig(heatmap_png_path, format='png', dpi=300)
    plt.savefig(heatmap_pdf_path, format='pdf', dpi=300)
    plt.close()

    return heatmap_png_path, heatmap_pdf_path

def main_pipeline(data_path, time_column, fluorescence_columns, output_dir):
    # Load data
    data = pd.read_csv(data_path)

    # Step 1: Preprocessing
    time, smoothed_data = preprocess_data(data, time_column, fluorescence_columns)

    # Step 2 & 3: Peak Detection and Characterization
    peak_details = detect_peaks(time, smoothed_data)

    # Step 4: Aggregated Statistics
    aggregated_stats = aggregate_peak_statistics(peak_details)

    # Save results
    peak_details_path, aggregated_stats_path = save_results(peak_details, aggregated_stats, output_dir)

    # Heatmap Visualization
    heatmap_png_path, heatmap_pdf_path = plot_heatmap(smoothed_data, time, output_dir)

    return {
        "Peak_Details_CSV": peak_details_path,
        "Aggregated_Stats_CSV": aggregated_stats_path,
        "Heatmap_PNG": heatmap_png_path,
        "Heatmap_PDF": heatmap_pdf_path
    }
