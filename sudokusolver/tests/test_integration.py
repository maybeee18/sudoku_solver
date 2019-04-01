#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:30:50 2019

@author: matthewgray
"""

import os, sys, unittest
#sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('sudokusolver'))

from detection_class import SudokuDetector
from digit_recognition import DigitRecognizer
from solver import SudokuSolver

# XMLrunner used to tie into Jenkins unit testing
import xmlrunner

class TestSudokuDetection(unittest.TestCase):
    
    def setUp(self):
        model_path = 'sudokusolver/models/cnn_digit_recognition.h5'
        self.sudokuDetector = SudokuDetector()
        self.digitRecognizer = DigitRecognizer(model_path=model_path)
        self.sudokuSolver = SudokuSolver()
        
    def test_ideal_image(self):
        
        # Test ideal online screenshot
        
        input_filepath = 'sudokusolver/tests/ideal_image.jpg'
        
        output_case = [[1, 6, 5, 9, 2, 8, 3, 4, 7],
                       [7, 2, 9, 4, 3, 1, 6, 8, 5],
                       [3, 8, 4, 5, 6, 7, 1, 2, 9],
                       [5, 3, 8, 2, 1, 4, 7, 9, 6],
                       [4, 1, 7, 6, 9, 5, 2, 3, 8],
                       [2, 9, 6, 8, 7, 3, 4, 5, 1],
                       [6, 7, 2, 3, 8, 9, 5, 1, 4],
                       [8, 5, 1, 7, 4, 2, 9, 6, 3],
                       [9, 4, 3, 1, 5, 6, 8, 7, 2]]
                       
        
        board_extract = self.sudokuDetector.detect_board(input_filepath)
        detected_board = self.digitRecognizer.recognize_board(board_extract)
        output_result = self.sudokuSolver.solveSudoku(detected_board)
        
        self.assertEqual(output_result, output_case)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)







# EOF
