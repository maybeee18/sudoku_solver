#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:27:34 2019

@author: matthewgray
"""

from keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
import PIL.ImageOps
import cv2

# Load model
model = load_model("cnn_digit_recognition.h5")

# TODO: Append own test dataset to get a sense of accuracy and how blank digits are handled
test_labels = 'LabeledDigits.csv'

df = pd.read_csv(test_labels)

filepath = '/Users/matthewgray/Desktop/SudokuSolver/sudokusolver/models/test_accuracy/digit-17.png'

def is_zero(filepath):
    # Take the inner 28x28 pixels and determine number of white pixels
    img = np.array(Image.open(filepath))
    
    # Crop out middle region to determine number of positive pixels
    img = img[14:(14+28), 14:(14+28)]
    
    black_inner_pixels = sum(sum(img>(255/2)))
    
    return black_inner_pixels

df['black_pixels'] = df['label'].apply(lambda x: is_zero(x))

test = df[['image_path', 'black_pixels']]

filepath = 'C:\\Users\\blamp\\Desktop\\AIML\\sudoku_solver\\sudokusolver\\models\\test_accuracy\\digit-15.png'
def load_image(filepath):
    # Convert to black for markings
    #img = PIL.ImageOps.invert(Image.open(filepath))
    img = Image.open(filepath)
    
#    # Cut some of the border
#    w, h = img.size
#    img = img.crop((10,7,w-10,h-7))

    # Erode image to suit MNIST style
    erode_kernel = np.array([[0, 1, 0],
                             [1, 1, 1],
                             [0, 1, 0]], dtype='uint8')
    
    eroded = cv2.erode(np.array(img), erode_kernel, iterations=3)
    #Image.fromarray(eroded)
    img = Image.fromarray(eroded)
    
    # Resize to get proper size
    img = img.resize((28,28))
    
    img = np.array(img)
    
#    # Crop out the middle 28x28 region
#    img = img[14:(14+28), 14:(14+28)]
    
    return img
    
df['img'] = df['label'].apply(lambda x: load_image(x))

# Need to convert to (?, 28, 28, 1) matrix for input to predict
imgs = df['img'].values

input_data = np.zeros((imgs.shape[0], 28, 28, 1))
for i, digit in enumerate(imgs):
    input_data[i, :, :, 0] = digit

values = np.round(model.predict(input_data), 2)


df['0'] = values[:,0]
df['1'] = values[:,1]
df['2'] = values[:,2]
df['3'] = values[:,3]
df['4'] = values[:,4]
df['5'] = values[:,5]
df['6'] = values[:,6]
df['7'] = values[:,7]
df['8'] = values[:,8]
df['9'] = values[:,9]

prediction = np.argmax(values, axis=1)
df['predict'] = prediction

# Manual override for black pixel counts > 250 based on empirical evidence
df['predict_override'] = (df['black_pixels'] > 250).astype(int)
df['prediction'] = df['predict']*df['predict_override']


test = df[['image_path', 'prediction']]

# How many zero digits are properly recognized?
zero_results = test[test['image_path'] == 0]
zero_accuracy = ((zero_results['prediction'] == 0).sum())/zero_results.shape[0]

print('Zero digit precision: ' + str(round(zero_accuracy*100, 2)) + '%')

# How many nonzero digits are properly recognized?

nonzero_results = test[test['image_path'] != 0]

nonzero_accuracy = ((nonzero_results['image_path'] == nonzero_results['prediction']).sum())/nonzero_results.shape[0]
print('Nonzero digit accuracy: ' + str(round(nonzero_accuracy*100, 2)) + '%')

# EOF
