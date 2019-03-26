#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:30:35 2019

@author: matthewgray
"""

import cv2
import numpy as np
from PIL import Image

# TODO: Convert all transformations to methods of a class object

# Load image in Grayscale
img_path = 'tests/newspaper_image.jpg'
img = cv2.imread(img_path, 0) # 0 Signifies grayscale (No RGB Values)

# Gaussian blur to smooth out the noise
blur_kernel_size = (5, 5)
blur_img = cv2.blur(img, blur_kernel_size)

# Thresholding the image
# Adaptive thresholding works well in various illumination settings
max_pixel_value = 255
block_size_for_adaptive_threshold = 5
threshold_subtraction_constant = 2

threshold_img = cv2.adaptiveThreshold(blur_img, max_pixel_value,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY,
                                      block_size_for_adaptive_threshold,
                                      threshold_subtraction_constant)

# Invert image to make borders white
inverted_img = cv2.bitwise_not(threshold_img)

# Dilate the image to restore broken lines due to thresholding operation
# Cross shaped kernel based on tutorial
dilate_kernel = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], dtype='uint8')
dilated_img = cv2.dilate(inverted_img, dilate_kernel)

Image.fromarray(dilated_img)







## Gaussian threshold test for sample case
#test_img = np.array([[190,160,120, 75, 50],
#                     [170,150,100, 40, 30],
#                     [140,130,200, 80, 20],
#                     [120, 90, 50, 20, 10],
#                     [100, 70, 35, 10,  5]], dtype='uint8')
#
#
#threshold_img = cv2.adaptiveThreshold(test_img, 255,
#                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                      cv2.THRESH_BINARY, 5, 2)


"""
DEBUG COMMANDS

Image.fromarray(img)

Image.fromarray(blur_img)

Image.fromarray(threshold_img)

Image.fromarray(inverted_img)

visualized_image = Image.fromarray(img)




#"""










# EOF
