#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 08:58:28 2019

@author: matthewgray
"""

# Read in all digit images and ask user for labels
# Output the results of all labels as a csv file
import os, sys
import pandas as pd
from PIL import Image
#from IPython.display import Image

import matplotlib.pyplot as plt

image_folder = 'test_accuracy'

label_collection = []

for root, dirs, files in os.walk(image_folder, topdown=False):
    for name in files:
        image_path = os.path.join(os.getcwd(), root, name)
        
        # Load image
        #Image(filename=image_path)
        current_img = Image.open(image_path)
        plt.imshow(current_img)
        plt.show()
#        
        # Get users label
        raw_label = int(input('Input Label: '))
        
        # Add to list
        label_collection.append([image_path, raw_label])

# Create pandas dataframe for writing as csv
df = pd.DataFrame(label_collection, columns={"image_path", "label"})

df.to_csv('LabeledDigits.csv', header=True, index=False)



# EOF
