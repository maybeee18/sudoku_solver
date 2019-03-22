#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:59:23 2019

@author: matthewgray
"""

import unittest

from SudokuSolving import solveSudoku

class TestSudokuSolver(unittest.TestCase):
    
    def test_easy_puzzle(self):
        
        # Test valid case #1
        
        input_case = [[5, 1, 7, 6, 0, 0, 0, 3, 4],
                      [2, 8, 9, 0, 0, 4, 0, 0, 0],
                      [3, 4, 6, 2, 0, 5, 0, 9, 0],
                      [6, 0, 2, 0, 0, 0, 0, 1, 0],
                      [0, 3, 8, 0, 0, 6, 0, 4, 7],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 9, 0, 0, 0, 0, 0, 7, 8],
                      [7, 0, 3, 4, 0, 0, 5, 6, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        output_case = [[5, 1, 7, 6, 9, 8, 2, 3, 4],
                       [2, 8, 9, 1, 3, 4, 7, 5, 6],
                       [3, 4, 6, 2, 7, 5, 8, 9, 1],
                       [6, 7, 2, 8, 4, 9, 3, 1, 5],
                       [1, 3, 8, 5, 2, 6, 9, 4, 7],
                       [9, 5, 4, 7, 1, 3, 6, 8, 2],
                       [4, 9, 5, 3, 6, 2, 1, 7, 8],
                       [7, 2, 3, 4, 8, 1, 5, 6, 9],
                       [8, 6, 1, 9, 5, 7, 4, 2, 3]]
        
        output_result = solveSudoku(input_case)
        
        self.assertEqual(output_result, output_case)
        
    def test_ver_difficult_puzzle(self):
        
        # Test taken from
        # http://www.7sudoku.com/view-puzzle?date=20190317
        
        input_case = [[9, 0, 0, 0, 2, 0, 7, 0, 0],
                      [0, 0, 0, 9, 0, 0, 1, 5, 0],
                      [4, 0, 0, 0, 0, 0, 0, 2, 0],
                      [0, 0, 0, 5, 0, 6, 0, 8, 0],
                      [0, 7, 0, 0, 0, 0, 0, 4, 0],
                      [0, 5, 0, 3, 0, 8, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0, 3],
                      [0, 8, 2, 0, 0, 1, 0, 0, 0],
                      [0, 0, 9, 0, 5, 0, 0, 0, 1]]
        
        output_case = [[9, 6, 1, 4, 2, 5, 7, 3, 8],
                       [7, 2, 8, 9, 6, 3, 1, 5, 4],
                       [4, 3, 5, 1, 8, 7, 6, 2, 9],
                       [1, 9, 4, 5, 7, 6, 3, 8, 2],
                       [8, 7, 3, 2, 1, 9, 5, 4, 6],
                       [2, 5, 6, 3, 4, 8, 9, 1, 7],
                       [5, 1, 7, 8, 9, 4, 2, 6, 3],
                       [6, 8, 2, 7, 3, 1, 4, 9, 5],
                       [3, 4, 9, 6, 5, 2, 8, 7, 1]]
        
        output_result = solveSudoku(input_case)
        
        self.assertEqual(output_result, output_case)
        

    def test_invalid_size(self):
        
        input_case = [[1,1,2],[2,1,3],[1,3,2]]
        
        output_result = solveSudoku(input_case)
        
        self.assertFalse(output_result)
        
    def test_invalid_type(self):
        
        input_case = 4
        
        output_result = solveSudoku(input_case)
        
        self.assertFalse(output_result)
        
    def test_unsolvable_case(self):
        
        input_case = [[5, 5, 5, 6, 0, 0, 0, 3, 4],
                      [5, 5, 5, 0, 0, 4, 0, 0, 0],
                      [5, 5, 5, 2, 0, 5, 0, 9, 0],
                      [6, 0, 2, 0, 0, 0, 0, 1, 0],
                      [0, 3, 8, 0, 0, 6, 0, 4, 7],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 9, 0, 0, 0, 0, 0, 7, 8],
                      [7, 0, 3, 4, 0, 0, 5, 6, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        output_result = solveSudoku(input_case)
        
        self.assertFalse(output_result)

if __name__ == '__main__':
    unittest.main()






# EOF
