# Calcium-analysis
<p align="center">GBM cells or nuclei are detected autonmatically by cellpose (GUI) to generate regions of interest (ROIs)</p>  
<p align="center">↓</p>  
<p align="center">Raw Fluorescence Data measured by imageJ </p>   
<p align="center">↓</p>  
<p align="center">Baseline Correction (ΔF/F) → Smoothing (Savitzky-Golay)</p>  
<p align="center">↓</p> 
<p align="center">Peak Detection (find_peaks)</p> 
<p align="center">↓</p> 
<p align="center">Extract Peak Characteristics:Amplitude, Width, Frequency, Period</p> 
<p align="center">↓</p> 
<p align="center">Aggregate Statistics (per region):  - Total Peaks
    - Mean Amplitude
    - Mean Width
    - Frequency
    - Mean Period</p> 


   
      ↓
Visualization:
    - Heatmaps
    - Trace Overlays
      ↓
Export Results:
    - Heatmap (PNG)
    - Detailed Peaks (CSV)
    - Aggregated Statistics (CSV)
