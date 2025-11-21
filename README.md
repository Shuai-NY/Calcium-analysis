# Calcium-analysis
<p align="center">GBM cells or nuclei are detected autonmatically by cellpose (GUI) to generate regions of interest (ROIs)</p>  
<p align="center">↓</p>  
<p align="center">Raw Fluorescence Data measured by imageJ </p>   
<p align="center">↓</p>  
<p align="center">Baseline Correction (ΔF/F) → Smoothing (Savitzky-Golay)</p>  
<p align="center">↓</p> 
Peak Detection (find_peaks)
      ↓
Extract Peak Characteristics:
    - Amplitude
    - Width
    - Frequency
    - Period
      ↓
Aggregate Statistics (per region):
    - Total Peaks
    - Mean Amplitude
    - Mean Width
    - Frequency
    - Mean Period
      ↓
Visualization:
    - Heatmaps
    - Trace Overlays
      ↓
Export Results:
    - Heatmap (PNG)
    - Detailed Peaks (CSV)
    - Aggregated Statistics (CSV)
