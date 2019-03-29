#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:30:50 2019

@author: matthewgray
"""

import os, sys, unittest
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('sudokusolver'))

from detection_class import SudokuDetector

# XMLrunner used to tie into Jenkins unit testing
import xmlrunner

class TestSudokuDetection(unittest.TestCase):
    
    def setUp(self):
        self.sudokuDetector = SudokuDetector()
    
#    def test_newspaper_image(self):
#        
#        # Test image taken from mobile camera on newspaper
#        
#        input_filepath = 'tests/newspaper_image.jpg'
#        
#        output_case = [[0, 0, 0, 6, 0, 4, 7, 0, 0],
#                       [7, 0, 6, 0, 0, 0, 0, 0, 9],
#                       [0, 0, 0, 0, 0, 5, 0, 8, 0],
#                       [0, 7, 0, 0, 2, 0, 0, 9, 3],
#                       [8, 0, 0, 0, 0, 0, 0, 0, 5],
#                       [4, 3, 0, 0, 1, 0, 0, 7, 0],
#                       [0, 5, 0, 2, 0, 0, 0, 0, 0],
#                       [3, 0, 0, 0, 0, 0, 2, 0, 8],
#                       [0, 0, 2, 3, 0, 1, 0, 0, 0]]
#        
#        output_result = self.sudokuDetector.detectSudoku(input_filepath)
#        
#        self.assertEqual(output_result, output_case)
        
    def test_ideal_image(self):
        
        # Test ideal online screenshot
        
        input_filepath = 'tests/ideal_image.jpg'
        
        output_case = [[0, 0, 0, 0, 0, 8, 0, 0, 0],
                       [7, 0, 0, 4, 0, 0, 6, 8, 0],
                       [3, 0, 0, 5, 0, 0, 0, 2, 0],
                       [0, 3, 0, 2, 0, 0, 0, 0, 6],
                       [4, 0, 0, 6, 0, 0, 0, 0, 0],
                       [0, 0, 6, 0, 7, 3, 4, 5, 0],
                       [0, 7, 0, 3, 0, 0, 0, 0, 0],
                       [0, 5, 1, 0, 0, 2, 0, 0, 0],
                       [9, 0, 0, 0, 5, 0, 8, 7, 0]]
        
        output_result = self.sudokuDetector.detect_board(input_filepath)
        
        self.assertEqual(output_result, output_case)
        
#    def test_image_with_background_colours(self):
#        
#        # Test online screenshot containing background colours
#        
#        input_filepath = 'tests/image_with_background_colours.png'
#        
#        output_case = [[0, 0, 0, 4, 0, 0, 0, 8, 0],
#                       [1, 9, 0, 6, 0, 0, 4, 5, 0],
#                       [0, 2, 0, 0, 8, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 0, 0, 0, 9, 7],
#                       [0, 0, 2, 0, 0, 0, 6, 0, 0],
#                       [8, 1, 0, 0, 0, 0, 0, 0, 0],
#                       [0, 0, 0, 0, 7, 0, 0, 6, 0],
#                       [0, 7, 3, 0, 0, 5, 0, 1, 9],
#                       [0, 4, 0, 0, 0, 9, 0, 0, 0]]
#        
#        output_result = self.sudokuDetector.detectSudoku(input_filepath)
#        
#        self.assertEqual(output_result, output_case)
   

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)







# EOF
