# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:52:18 2019

@author: blamp
"""

import cv2
import numpy as np
from PIL import Image
from scipy.spatial import distance as dist

class SudokuDetector():
    
    def _load_image(self, img_path):
        # Load image in Grayscale
        # 0 Signifies grayscale (No RGB Values)
        return cv2.imread(img_path, 0)
    
    def _blur_image(self, img, kernel_size=(5, 5)):
        return cv2.blur(img, kernel_size)
    
    def _threshold_image(self, img, max_pixel_value=255,
                         block_size_for_adaptive_threshold=11,
                         threshold_subtraction_constant=2):
        # Adaptive thresholding works well in various illumination settings
        threshold_img = cv2.adaptiveThreshold(img, max_pixel_value,
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY,
                                              block_size_for_adaptive_threshold,
                                              threshold_subtraction_constant)
        
        return threshold_img
    
    def _invert_image(self, img):
        # TODO: Detect whether or not image should be inverted
        return cv2.bitwise_not(img)
    
    def _dilate_image(self, img):
        # Dilate the image to restore broken lines due to thresholding operation
        # Cross shaped kernel based on tutorial
        dilate_kernel = np.array([[0, 1, 0],
                                  [1, 1, 1],
                                  [0, 1, 0]], dtype='uint8')
        
        dilated_img = cv2.dilate(img, dilate_kernel)
        return dilated_img
    
    def _warp_image(self, img):
        
        # Detect blobs via contours in image
        im2, contours, hierarchy = cv2.findContours(img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        
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
        
        warped_img = cv2.warpPerspective(img, new_perspective, (image_size, image_size))

        return warped_img
    
    def _segment_image(self, img):
        
        # Extract individual digits
        img_shape = img.shape
        image_size = img_shape[0]
        
        # Loop to pull individual images
        x_shift = image_size/9
        y_shift = image_size/9
        
        # Create blank list to store rows
        output_array = []
        
        for y_digit in np.arange(9):
            
            # Create list to store columns
            column_digits = []
            
            for x_digit in np.arange(9):
                
                x_lower = int(x_shift*x_digit)
                x_upper = int(x_shift*(x_digit+1))
                
                y_lower = int(y_shift*y_digit)
                y_upper = int(y_shift*(y_digit+1))
                
                digit_img = img[y_lower:y_upper, x_lower:x_upper]
                
                column_digits.append(digit_img)
                
            # After each column loop, fill the values in the output array as a row
            output_array.append(column_digits)
                
                # 
                
                # Debug line, print out all digits for test accuracy
                #Image.fromarray(digit_img).save("digit-" + str(digit_index) + ".png")
        
        return output_array
    
    def detect_board(self, img_path):
        img = self._load_image(img_path)
        blurred_img = self._blur_image(img)
        black_white_img = self._threshold_image(blurred_img)
        inverted_img = self._invert_image(black_white_img)
        dilated_img = self._dilate_image(inverted_img)
        warped_img = self._warp_image(dilated_img)
        board_array = self._segment_image(warped_img)
        
        return board_array
    
if __name__ == '__main__':
    detector = SudokuDetector()
    board = detector.detect_board('tests/ideal_image.jpg')
    
    # Show image
    Image.fromarray(board[0][0])


    