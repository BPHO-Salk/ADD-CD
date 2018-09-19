# ADD-CD
Analysis of Distance Distributions by Contour Dilations

This program was written for the qunatitative analysis of distances between mitochondria and associated endoplasmic reticulum from transmission electron micrographs for the paper *Regulation of the cell stress response by the microprotein PIGBOS* (Qian Chu, et. al., under revision). 

This package is meant to serve two functions: 

[1] To provide a method to **binarize traces** of mitochondrial and endoplasmic reticulum contour traces, using TrakEM2 [a]. Binary traces are exported as *.tiff* files using a Beanshell macro code provided by John Bogovic [b]. Finally, trace file names are formatted in Python for use in function [2]. 

[2] To provide a **quantitative analysis of the distribution of distances** between a mitochondrion trace and the contour trace of associated endoplasmic reticulum. This is achieved by dilating the contour of a mitochondrion trace one pixel at a time 100 times and plotting the distribution of dilated pixels that overlap with the ER trace. 

### Software requirements
[1] ImageJ/Fiji (http://www.fiji.sc/downloads)

[2] Anaconda (https://www.anaconda.com/download/) or a distribution of Python with the following packages: Pillow*, Matplotlib, Numpy, XLWT, SciPy, OS, Pandas, Shutil

\* All of these packages come deployed with Anaconda, except for Pillow which can be installed by opening the Anaconda Prompt and installing it using the following line of code: *pip install Pillow*

### Autodidactic testing

Download the GitHub repository to your harddrive. Copy images from *theoreticalTest* to *images*. 

Open ADD-CD.py in Spyder (or your favorite IDE). Read comments and code and run the script. Output will be stored in an Excel file under *output/excel*

### [1] Binarizing traces
In the TrakEM2 folder, open trakEM2example.xml with Fiji to see an example of how to set up your project for tracing. 

Import a new image of your own to a new layer. Make sure that you note the pixel size (in nanometers) for each image. All downstream analysis will return pixel-wise results that will need to be scaled according to your effective resolution. Consider scaling your input image to 1 nm pixels before starting to simplify analysis. 

Add a new *anything* layer from the template to the project. Add new *mnumber*, *mitochondria*, and *er* layers to the *id* layer you added to the project. Note the tree structure - each *er* trace is associated with a *mitochondria* which is associated with an *mnumber* which is associated with an *id*. Multiple *mnumber*s can be associated with a single *id* - only a single *mitochondria* trace should be associated with a given *mnumber*, and only a single *er* trace should be associated with a given *mitochondria*. 

Rename the *id* layer and *mnumber* layers for every new condition (id) and mitochondria (mnumber) for which you make traces. Add area lists to the *mitochondria* and *er* layers. Using the brush, hold shift and use the mouse wheel to change the brush size. 

Trace the mitochondria and ER profiles with their respective area lists selected according to the template. **NB:** It is critical that the brush size for ER traces is set to 1 px (the smallest setting). Trace only the contour of the ER nearest to the mitochondria. 

Once all traces are complete, open the file *TrakEM2binaryExport-JohnBogovic.bsh* in Fiji. It will open the Fiji macro prompt. Change the folder *destdir="C:/Users/path/to/the/working/folder/ADD-CD/trakEM2/binaryOutput/";* to the appropriate folder. If you downloaded the package to your desktop, change the path to *path/to/your/desktop/ADD-CD/trakEM2/binaryOutput/";* -- this will simplify the next steps. 

Once you have specified the appropriate folder, press the *Run* button in the bottom left. You now have binarized traces for further processing. 

Next, open the file *renameTrakEM2outputForAnalysis.py* in Spyder (Anaconda). If you used the folder format specified above, you should be able to run the program. In the *trakEM2/processedOuput* subfolder, you will have your mitochondria and ER binarized trace files (.tiff format) with the naming scheme: *184 - m1 - mitochondria.tiff* or *184 - m1 - ER.tiff*. These images can now be used in the ADD-CD analysis program. 

### [2] Quantitative analysis of the distribution of distances by contour dilation

Copy the binarized images from *ADD-CD/trakEM2/processedOutput* to *ADD-CD/images*. Open *ADD-CD.py* in Spyder (Anaconda), and run the program. You now have a distribution of distances between the two contours, saved into an excel worksheet under *ADD-CD/output/excel/output.xls*. 


### References

[a] (Cardona, Albert, et al. "TrakEM2 software for neural circuit reconstruction." PloS one 7.6 (2012): e38011.

[b] Thread from ImageJ forum with John Bogovic, including his original code: https://forum.image.sc/t/trakem2-scripting-export-arealists-as-tiffs-with-template-architecture/9461/10
