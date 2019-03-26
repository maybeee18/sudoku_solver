#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:30:35 2019

@author: matthewgray
"""

import cv2
import numpy as np
from PIL import Image
from scipy.spatial import distance as dist

# TODO: Convert all transformations to methods of a class object

# TODO: opencv-python==3.4.5.20 required for drawKeypoints command

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

# Detect blobs via contours in image
im2, contours, hierarchy = cv2.findContours(dilated_img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

# Hack to pick out the 4 best bounding points of the sudoku board
biggest = None
max_area = 0
for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                        biggest = approx
                        max_area = area

## Show the bounding polygon overtop the dilated image
#Image.fromarray(cv2.polylines(dilated_img, [biggest], True, (125,125,125), 5))
    
 
# Reorder the polygon coordinates in proper order for warping tranformation
def order_points(pts):
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
 
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
 
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
 
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
 
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, bl, br], dtype="float32")    
    
    
# Compute a perspective transformation to straighten the image
image_size = 500    

pts1 = np.array([order_points(np.squeeze(biggest))])
pts2 = np.float32([[0,0],[image_size,0],[0,image_size],[image_size,image_size]])

new_perspective = cv2.getPerspectiveTransform(pts1, pts2)

warped_img = cv2.warpPerspective(dilated_img, new_perspective, (image_size, image_size))










"""
DEBUG COMMANDS

Image.fromarray(img)

Image.fromarray(blur_img)

Image.fromarray(threshold_img)

Image.fromarray(inverted_img)

Image.fromarray(dilated_img)

Image.fromarray(warped_img)



#"""










# EOF
