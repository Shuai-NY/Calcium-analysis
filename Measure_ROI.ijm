// Set the working directory
dir = getDirectory("Choose a Folder");

// Get list of all .tif files
list = getFileList(dir);

for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif")) {
        imageName = list[i];
        baseName = replace(imageName, ".tif", "");
        
        // Construct corresponding ROI path
        roiFile = dir + "MAX_" + baseName + "_rois.zip";
        if (!File.exists(roiFile)) {
            print("ROI file not found for: " + imageName);
            continue;
        }

        // Open image
        open(dir + imageName);
        selectWindow(imageName);

        // Load ROIs
        roiManager("reset");
        roiManager("Open", roiFile);

        // Run measurements
        roiManager("Multi Measure");

        // Save results
        saveAs("Results", dir + baseName + ".csv");

        // Clean up
        run("Close All");
        roiManager("reset");
    }
}
