// ===== Select Directories =====
InputDir = getDirectory("Choose Source Directory");
OutputDir = getDirectory("Choose Destination Directory");
list = getFileList(InputDir);
setBatchMode(true);

// ===== Loop through all .vsi files =====
for (i = 0; i < list.length; i++) {
    filename = list[i];
    if (endsWith(filename, ".vsi")) {
        fullPath = InputDir + filename;
        baseName = replace(filename, ".vsi", "");

        // Open the .vsi file
        open(fullPath);
        setOption("ScaleConversions", true);

        // Select the GFP subimage
        selectImage(filename + " - GFP");
        run("8-bit");

        // Save as 8-bit TIFF
        saveAs("Tiff", OutputDir + baseName + " - GFP.tif");

        // Z projection
        run("Z Project...", "projection=[Max Intensity]");
        saveAs("Tiff", OutputDir + "MAX_" + baseName + " - GFP.tif");

        // Fire LUT and PNG export
        run("Fire");
        run("Scale Bar...", "width=50 height=50 font=50 bold overlay");
        saveAs("PNG", OutputDir + "MAX_" + baseName + " - GFP.png");

        // Cleanup: close projection
        close();
               // Re-select the saved TIFF
        selectImage(baseName + " - GFP.tif");
        run("Fire");
        run("Label...", "format=00:00 starting=0 interval=2 x=5 y=20 font=100 text=[] range=1-600");
        run("Scale Bar...", "width=50 height=50 font=50 bold overlay label");
        labelText = getString("Enter label text:", baseName);
        run("Label...", "format=Text starting=0 interval=2 x=325 y=105 font=100 text=" + labelText + " range=151-600");

        // Export AVI
        run("AVI... ", "compression=JPEG frame=40 save=[" + OutputDir + baseName + " - GFP.avi]");

        // Close image
        close();
    }
}
