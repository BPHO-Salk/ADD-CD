# ADD-CD
Analysis of Distance Distributions by Contour Dilations

This program was written for the qunatitative analysis of distances between mitochondria and associated endoplasmic reticulum from transmission electron micrographs for the paper *Regulation of the cell stress response by the microprotein PIGBOS* (Qian Chu, et. al., under revision). 

This package is meant to serve two functions: 

[1] To provide a method to **binarize traces** of mitochondrial and endoplasmic reticulum contour traces, using TrakEM2 [a]. Binary traces are exported as *.tiff* files using a Beanshell macro code provided by John Bogovic [b]. Finally, trace file names are formatted in Python for use in function [2]. 

[2] To provide a **quantitative analysis of the distribution of distances** between a mitochondrion trace and the contour trace of associated endoplasmic reticulum. This is achieved by dilating the contour of a mitochondrion trace one pixel at a time 100 times and plotting the distribution of dilated pixels that overlap with the ER trace. 

### Software Requirements
[1] ImageJ/Fiji (http://www.fiji.sc/downloads)

[2] Anaconda (https://www.anaconda.com/download/) or a distribution of Python with the following packages: Pillow*, Matplotlib, Numpy, XLWT, SciPy, OS, Pandas, Shutil

\* All of these packages come deployed with Anaconda, except for Pillow which can be installed by opening the Anaconda Prompt and installing it using the following line of code: *pip install Pillow*

### Autodidactic Testing

Download the GitHub repository to your harddrive. Copy images from *theoreticalTest* to *images*. 

Open ADD-CD.py in Spyder (or your favorite IDE). Read comments and code and run the script. Output will be stored in an Excel file under *output/excel*

### [1] Binarizing Traces
In the TrakEM2 folder, open trakEM2example.xml

### References

[a] (Cardona, Albert, et al. "TrakEM2 software for neural circuit reconstruction." PloS one 7.6 (2012): e38011.

[b] Thread from ImageJ forum with John Bogovic, including his original code: https://forum.image.sc/t/trakem2-scripting-export-arealists-as-tiffs-with-template-architecture/9461/10
