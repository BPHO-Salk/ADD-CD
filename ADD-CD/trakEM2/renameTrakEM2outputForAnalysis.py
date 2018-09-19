# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:31:38 2018

@author: sweisernovak
"""

from shutil import copyfile
import os

#filepath = r'\\bpho\Sammy Weiser Novak\TEM Imaging Data\QC PBL-A\March 2018 Prep\Cells\analysis\JpegAreaLists\134';

#filepath = '/'.join(filepath.split('\\'));


#os.chdir("//bpho-tera.ad.salk.edu" + filepath);

""" 
# Mitochondria format:   _trakEM2example.xml.gz_anything_1_m1_mitochondria_area list #21
# ER format:             _trakEM2example.xml.gz_anything_1_m1_mitochondria_er_area list #23

# Desired output format: ID - mNumber - contourType(mitochondria/ER)
"""

filepath = "binaryOutput/"
outputpath = "processedOutput/"

for filename in os.listdir(filepath):
    #print(filename)

    if filename.endswith(".tiff"):
        nameSplit = filename.split("_");
        ID  = nameSplit[3]
        mNumber = nameSplit[4]
        if nameSplit[6] == "er":
            contourType = "ER"
        else: 
            contourType = "mitochondria"
        
        newName = outputpath + ID + " - " + mNumber + " - " + contourType + ".tiff"
        print(newName)
        filename = filepath+filename;
        
        copyfile(filename, newName)    
