# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:18:04 2019

@author: blamp
"""

from keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
import PIL.ImageOps
import cv2

class DigitRecognizer():
    
    def __init__(self, model_path="models/cnn_digit_recognition.h5"):
        self.model = load_model(model_path)
        
    def _transform_digit_image(self, img):
        
        # Erode image to suit MNIST style
        erode_kernel = np.array([[0, 1, 0],
                                 [1, 1, 1],
                                 [0, 1, 0]], dtype='uint8')
        
        eroded_img = Image.fromarray(cv2.erode(np.array(img), erode_kernel, iterations=3))
        
        # Resize to get proper size
        transformed_img = np.array(eroded_img.resize((28,28)))
        
        return transformed_img
        
    def _crop_image(self, img):
        # Crop out middle region to determine number of positive pixels
        return img[14:(14+28), 14:(14+28)]
        
    def _is_zero(self, img):
        
        cropped_img = self._crop_image(img)
        
        num_white_inner_pixels = sum(sum(cropped_img<(255/2)))
        
        if num_white_inner_pixels > 400:
            return True
        else:
            return False
        
    def _score_digit(self, img):
        
        transformed_img = self._transform_digit_image(img)
        
        # Force image into 4D dimensionality for model input
        model_input = np.zeros((1, 28, 28, 1))
        model_input[0, :, :, 0] = transformed_img
        
        digit = np.argmax(self.model.predict(model_input))
        
        return digit
    
    def recognize_digit(self, img):
        
        if self._is_zero(img):
            return 0
        
        return self._score_digit(img)
    
    def recognize_board(self, board):
        recognized_board = np.zeros((9, 9))
        
        for x_index, row in enumerate(board):
            for y_index, column in enumerate(row):
                recognized_board[x_index, y_index] = self.recognize_digit(column)
                
        # Output format should be list of list for solver algorithm
        return recognized_board.tolist()

if __name__ == '__main__':
    recognizer = DigitRecognizer()
    
    import sys
    np.set_printoptions(threshold=sys.maxsize)
    
    print(recognizer.recognize_board(board))
