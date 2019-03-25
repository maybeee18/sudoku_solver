#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:40:18 2019

@author: matthewgray
"""

def validInput(grid):
    # Grid type should be 9x9 only considering list of lists for now
    if isinstance(grid, list):
        if len(grid) == 9:
            if (False in [len(x) == 9 for x in grid]) == False:
                return True
    return False
        

def findNextCellToFill(grid, i, j):
        for x in range(i,9):
                for y in range(j,9):
                        if grid[x][y] == 0:
                                return x,y
        for x in range(0,9):
                for y in range(0,9):
                        if grid[x][y] == 0:
                                return x,y
        return -1,-1

def isValid(grid, i, j, e):
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
                columnOk = all([e != grid[x][j] for x in range(9)])
                if columnOk:
                        # finding the top left x,y co-ordinates of the section containing the i,j cell
                        secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                        for x in range(secTopX, secTopX+3):
                                for y in range(secTopY, secTopY+3):
                                        if grid[x][y] == e:
                                                return False
                        return True
        return False

def solveSudoku(grid, i=0, j=0):
    
    # Only solve valid boards
    if validInput(grid):
    
        i,j = findNextCellToFill(grid, i, j)
        if i == -1:
                return True
        for e in range(1,10):
                if isValid(grid,i,j,e):
                        grid[i][j] = e
                        if solveSudoku(grid, i, j):
                                return grid
                        # Undo the current cell for backtracking
                        grid[i][j] = 0
    return False
    
# TODO: Create medium and hard sudoku puzzles
# TODO: Create unsolvable puzzle

#input = [[5,1,7,6,0,0,0,3,4],[2,8,9,0,0,4,0,0,0],[3,4,6,2,0,5,0,9,0],[6,0,2,0,0,0,0,1,0],[0,3,8,0,0,6,0,4,7],[0,0,0,0,0,0,0,0,0],[0,9,0,0,0,0,0,7,8],[7,0,3,4,0,0,5,6,0],[0,0,0,0,0,0,0,0,0]]
#solveSudoku(input)
#
#
#test_input2 = [[0,1,5,8,0,0,0,3,0],[0,6,2,0,4,0,1,0,0],[3,8,0,7,0,2,0,6,9],[4,0,0,0,0,8,0,0,1],[0,3,0,0,0,0,0,4,0],[2,0,0,1,0,0,0,0,5],[6,9,0,2,0,5,0,1,4],[0,0,1,0,7,0,6,2,0],[0,2,0,0,0,1,9,5,0]]
#solveSudoku(test_input2)
#
#test_input2_solution = [[7,1,5,8,9,6,4,3,2],[9,6,2,5,4,3,1,8,7],[3,8,4,7,1,2,5,6,9],[4,5,9,6,2,8,3,7,1],[1,3,8,9,5,7,2,4,6],[2,7,6,1,3,4,8,9,5],[6,9,3,2,8,5,7,1,4],[5,4,1,3,7,9,6,2,8],[8,2,7,4,6,1,9,5,3]]
#
#assert(test_input2 == test_input2_solution)



# EOF
