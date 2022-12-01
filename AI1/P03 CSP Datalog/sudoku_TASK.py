# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 08:13:32 2017

Formulates sudoku as a CSP, solving the riddle from
https://www.sudoku.ws/hard-1.htm as an example.

@author: stdm
@modif: tugg
"""

import sys

import pandas as pd
import time

sys.path.append("./python-constraint-1.2")
import constraint as csp

# ------------------------------------------------------------------------------
# sudoku to solve (add "0" where no number is given)
# ------------------------------------------------------------------------------
riddle_1 = [[0,0,0,2,0,0,0,6,3],
             [3,0,0,0,0,5,4,0,1],
             [0,0,1,0,0,3,9,8,0],
             [0,0,0,0,0,0,0,9,0],
             [0,0,0,5,3,8,0,0,0],
             [0,3,0,0,0,0,0,0,0],
             [0,2,6,3,0,0,5,0,0],
             [5,0,3,7,0,0,0,0,8],
             [4,7,0,0,0,1,0,0,0]]

# Difficult riddle
riddle = [[0,0,9,7,4,8,0,0,0],
             [7,0,0,0,0,0,0,0,0],
             [0,2,0,1,0,9,0,0,0],
             [0,0,7,0,0,0,2,4,0],
             [0,6,4,0,1,0,5,9,0],
             [0,9,8,0,0,0,3,0,0],
             [0,0,0,8,0,3,0,2,0],
             [0,0,0,0,0,0,0,0,6],
             [0,0,0,2,7,5,9,0,0]]

# ------------------------------------------------------------------------------
# create helpful lists of variable names
# ------------------------------------------------------------------------------
rownames = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(i+j)
    rows.append(row)

cols = []
for j in colnames:
    col = []
    for i in rownames:
        col.append(i+j)
    cols.append(col)

boxes = []
for x in range(3):  # over rows of boxes
    for y in range(3):  # over columns of boxes
        box = []
        for i in range(3):  # over variables in rows (in a box)
            for j in range(3):  # over variables in cols (in a box)
                box.append(rownames[x*3 + i] + colnames[y*3 + j])
        boxes.append(box)


# ------------------------------------------------------------------------------
# formulate sudoku as CSP
# ------------------------------------------------------------------------------


# Instantiate a solver from the file constraint.py: Which one may be meaningful?

# Problem solver with backtracking capabilities
solver = csp.BacktrackingSolver()

# Recursive problem solver with backtracking capabilities
# solver = csp.RecursiveBacktrackingSolver()

# From the class description:
	
"""
Recursive problem solver with backtracking capabilities

Examples:

>>> result = [[('a', 1), ('b', 2)],
...           [('a', 1), ('b', 3)],
...           [('a', 2), ('b', 3)]]

>>> problem = Problem(RecursiveBacktrackingSolver())
>>> problem.addVariables(["a", "b"], [1, 2, 3])
>>> problem.addConstraint(lambda a, b: b > a, ["a", "b"])

>>> solution = problem.getSolution()
>>> sorted(solution.items()) in result
True

>>> for solution in problem.getSolutions():
...     sorted(solution.items()) in result
True
True
True

>>> problem.getSolutionIter()
Traceback (most recent call last):
    ...
NotImplementedError: RecursiveBacktrackingSolver doesn't provide iteration
"""

# Problem solver based on the minimum conflicts theory
# This solver does not work, it provides only a single solution
# solver = csp.MinConflictsSolver()

# Code snippet is already provided
# Instantiate a sudoku i.e a problem with the chosen solver
# problem = Problem(RecursiveBacktrackingSolver())
sudoku = csp.Problem(solver)

# Use variable names from above: "Create helpful lists of variable names"
# Print Sudoku field from above: "Sudoku to solve (add "0" where no number is given)"
# "riddle" is needed to initialise, add constraints and fill the sudoku.
df = pd.DataFrame(riddle)
print(df)

# problem.addVariables(["a", "b"], [1, 2, 3])
for i in rownames:
    for j in colnames:
        sudoku.addVariable(i+j, list(range(1, 10)))
        print(f'Variable {str(i+j)} is added at {list(range(1, 10))}')

# problem.addConstraint(lambda a, b: b > a, ["a", "b"])
for i in range(9):
    for j in range(9):
        if riddle[i][j] != 0:
            sudoku.addConstraint(csp.InSetConstraint([riddle[i][j]]), [rownames[i]+colnames[j]])
            print("constraint %s is in set %s"%([riddle[i][j]],[rownames[i]+colnames[j]]))

# Add constrains to the nine rows, columns and  3 x 3 boxes
# CLass AllDifferentConstraint:
# Constraint enforcing that values of all given variables are different
for i in range(9):
    sudoku.addConstraint(csp.AllDifferentConstraint(), rows[i])
    print("all different constraint in %s" % rows[i])
    sudoku.addConstraint(csp.AllDifferentConstraint(), cols[i])
    print("all different constraint in %s" % cols[i])
    sudoku.addConstraint(csp.AllDifferentConstraint(), boxes[i])
    print("all different constraint in %s" % boxes[i])


# ------------------------------------------------------------------------------
# solve CSP
# ------------------------------------------------------------------------------
start = time.time()
# solution = problem.getSolution()
"""
Find and return a solution to the problem

Example:

>>> problem = Problem()
>>> problem.getSolution() is None
True
>>> problem.addVariables(["a"], [42])
>>> problem.getSolution()
{'a': 42}

@return: Solution for the problem
@rtype: dictionary mapping variables to values
"""
solutions = sudoku.getSolutions()
solution=solutions[0]

# Print aspects of the solution
print("Solution:")
print('Solution as dictionary:\n',solution)
print('Row names:\n', rownames)
print('Column names:\n', colnames, '')

print('\nSudoku board with solution:')
for i in rownames:
    for j in colnames:
        print(solution[i+j],end=', ')
    print()


end = time.time()
print(end - start)


# Given puzzle from the lab
# Time for csp.BacktrackingSolver()
# 0.01914381980895996

# Time for csp.RecursiveBacktrackingSolver()
# 0.024403095245361328

# Extreme Sudoku Puzzle 1 from https://www.sudoku.ws/extreme-1.htm
# Time for csp.BacktrackingSolver()
# 0.008357048034667969

# Time for csp.RecursiveBacktrackingSolver()
# 0.010776758193969727

# Findings
# It looks as the non-recursive solutin is faster than the recursive one. At least for the tested levels.