# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 16:12:21 2018

@author: sweisernovak, umanor

Notes: 
    - Analysis is done pixel-wise. All images should all have the same effective resolution before analysis. 
    - Test images are included in the subfolder "theoreticalTest" (see comments next to filepath and outputpath)
    - Input image formats should be as follows: "ID - mNumber - ER/mitochondria"  (eg. "184 - m1 - ER - SER" or "184 - m1 - mitochondria")

"""

from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import xlwt as xl
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
import os
import pandas as pd

# Initalize the Excel output sheet
book = xl.Workbook(encoding="utf-8")


# Definte the file paths for input (image locations) and output (figures and excel worksheets)
filepath = "images/" # Put your images in the "images folder." To test the algorithm and see how it works, copy the images from "theoretical test" into "images"
outputpath = "output" # Output path. Will output figures and Excel sheets

# Note: image name format: "184 - m1 - ER - SER" or "184 - m1 - mitochondria"

pixelSize = 1 # pixel size in nanometers -- Note: this program currently analyzes by pixels. Images should all be at same effective resolution before analysis! 

imageInfo = []

for filename in os.listdir(filepath):
    if filename.endswith(".tiff"):  # Note: Filetype must be .tiff, not .tif or any other image format. PIL image dependancy. 
        imageInfo.append(filename.split(" - "));
        
imageInfo = pd.DataFrame(imageInfo, columns=['id','mNumber','contourType']) 
#print(imageInfo)

idGroup = [] # create a group of all of the unique identifiers to be analyzed (ie., cell identifiers)
for row in imageInfo['id']:
    idGroup.append(row)
idIndex = np.unique(idGroup) # index of unique IDs used in naming scheme

for i, row in enumerate(idIndex): # looping through the unique IDs
    idGroup = imageInfo[imageInfo['id'] == idIndex[i]] 
    #print(idGroup) # test to see if all of the mitochondria and ERs are associated with eachother through their IDs
    
    ID = idIndex[i]
    #print(ID)
    
    
    mGroup = [] # group of mitochondria associated with a given ID
    for row in idGroup['mNumber']:
        mGroup.append(row)
        mIndex = np.unique(mGroup); # index of unique mitochondria associated with a given ID
    mNumber = mIndex[0]
    print(mNumber)
    #print(mIndex)
    
    for i, row in enumerate(mIndex): # loop through the mitochondria associated with a given ID
        
        mGroup = idGroup[idGroup['mNumber'] == mIndex[i]] # looping through this group of mitochondria one by one
                
        #raise SystemExit(0)
        
        # Mitochondria condition (If we are looking at an image mitochondrion trace, not ER)
        
        # Reconstruct the file name
        
        mitoName = mGroup[mGroup['contourType'] == 'mitochondria.tiff'].to_string(header=False,index=False,index_names=False) # make sure we are looking just at mitochondria (not ER) and output the file name
        nameSplit = mitoName.split('  ') # split along spaces 
        mitoName = ' - '.join(nameSplit) # and join back with dases to achieve the original filename
        #print(mitoName) # should print outthe file name (ie., 1 - m1 - mitochondria.tif)
            
        mitoArray = Image.open(filepath+mitoName) # import the mitochondrial profile .tiff
        mitoArray = mitoArray.convert('L') # convert to grayscale
        mitoArray = mitoArray.point(lambda x: 0 if x<128 else 255, '1') # threshold and set mitochondria pixels to '1'
        mitoArray = np.array(mitoArray).astype(int) # convert to an array of integers (not booleans)
        mitoAreaPixelValue = np.sum(mitoArray)
        #print(mitoArray)
        
        erodedMitoArray = erode(mitoArray).astype(int) # create an eroded version of the mitochondria (eroded by 1 pixel by default)
        #print(erodedMitoArray)
        
        mitoPerimeterArray = mitoArray - erodedMitoArray # create a perimeter profile of the mitochondria
        #print(mitoPerimeterArray)
        #plt.imshow(mitoPerimeterArray) 
        #plt.show() # should print out the perimeter of the mitochondria
        
        mitoPerimeterPixelValue = np.sum(mitoPerimeterArray) # total number of pixels in the mitochondrial perimeter
        #print("Total mitochondrial perimeter pixels: ", mitoPerimeterPixelValue)

        ### Generating the array of mitochondrial dilation contours 
        
        dilationFactor = 1  ; # number of pixels to dilate each contour by
        contourNumber  = 100; #number of countours to make
                
        mitoDilated = dilate(mitoArray).astype(int); #the first dilation
        #print(mitoDilated)
        
        dilatedArray = [mitoDilated]; # array to hold subsequent dilations
        
        newDilated = mitoDilated;
        
        for x in range(contourNumber): # this loop will fill the dilatedArray with ### "contourNumber" of dilated contours, each dilated by "dilationFactor"
            newDilated = dilate(newDilated, iterations=dilationFactor).astype(int);
            dilatedArray.append(newDilated);
        
        ### ER condition
    
               
        ERname = mGroup[mGroup['contourType'] == 'ER.tiff'].to_string(header=False,index=False,index_names=False)
        ERname = ERname.split('  ')
        ERname = ' - '.join(ERname)
        
        ERarray = Image.open(filepath+ERname)
        ERarray = ERarray.convert('L') # convert to grayscale
        ERarray = ERarray.point(lambda x: 0 if x<128 else 255, '1') # threshold and set ER pixels to '1'
        ERarray = np.array(ERarray).astype(int) # convert to an array of integers (not booleans)
        #print(ERarray)
        
        ERcountPixelValue = np.sum(ERarray)
        #print("Total ER pixels: ", ERcountPixelValue);
        
        #raise SystemExit(0)
        
        ### Creating combined mitochondria-ER contour set
        
        
        ERmitoArray = ERarray + mitoArray
        ADDarray = [ERmitoArray]
        
        combinedArray = []
        overlapPixelsArray = []
        # i = 0 # iteration number, if we ever need a counter
        
        for mArray in dilatedArray:
            combinedArray = mArray + ERarray # find the sum of the mitochondrial and ER contour arrays -- pixels == 2 are overlaps
            overlapPixels = np.count_nonzero(combinedArray == 2); # number of pixels where the dilated mitochondrial contour overlaps with the ER contour
            overlapPixelsArray.append(overlapPixels) # append the overlap map to the list of overlap maps
            # i = i + 1 # increase the iteration number
            ADDarray.append(combinedArray) # analysis of distance distributions according to sequential the dilations
        
        
        # uncomment this block to see the calculated distribution of distances between mitochondria and ER (measured in pixels)
        #print(overlapPixelsArray)
        #plt.bar(np.arange(101), overlapPixelsArray)
        #plt.show()
        
        # uncomment this block to see the mito and ER traces followed by the first two dilation iterations
        #print(ADDarray[0])
        plt.imshow(ADDarray[0]) # show the mitochondria and ER traces
        plt.show()
        #plt.imshow(ADDarray[1]) 
        #plt.show()
        #plt.imshow(ADDarray[2]) 
        #plt.show()
        #raise SystemExit(0)
        
        ### Excel output
        
        
        # Testing names for all of the parameters before saving
        print(ID, mNumber, mitoPerimeterPixelValue, mitoAreaPixelValue, ERcountPixelValue, dilationFactor, contourNumber)
        # Checking the overlap values for the dilations
        print(overlapPixelsArray)
        
        #raise SystemExit(0)
        
        bookName = str(ID + " - " + mNumber)
        
        sheet1 = book.add_sheet(bookName)
        
        sheet1.write(0, 0, "ID")
        sheet1.write(1, 0, "mNumber")
        sheet1.write(2, 0, "Mito Perimeter")
        sheet1.write(3, 0, "Mito Area")
        sheet1.write(4, 0, "ER Length")
        sheet1.write(5, 0, "Dilation Factor")
        sheet1.write(6, 0, "Number of Contours")
        
        sheet1.write(8, 0, "Analysis of Distance Distributions")
        #raise SystemExit(0)
        
        sheet1.write(0, 1, ID)
        sheet1.write(1, 1, str(mNumber))
        sheet1.write(2, 1, str(mitoPerimeterPixelValue))
        sheet1.write(3, 1, str(mitoAreaPixelValue))
        sheet1.write(4, 1, str(ERcountPixelValue))
        sheet1.write(5, 1, str(dilationFactor))
        sheet1.write(6, 1, str(contourNumber))
                
        for i,e in enumerate(overlapPixelsArray):
            sheet1.write(8,i+1,str(e))
        
bookname = outputpath + "/excel/ output.xls";
#raise SystemError(0)
book.save(bookname);

        
        
               
        
       
