import game
import math
import numpy as np
import sys

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

# Constants to end the recursion
DEPTH_LIMIT = 2
LOW_PROBABILITY = 0.00000000001

# Constants to calculate the score.
SCORE_SUM_POWER = 3.5
SCORE_MONOTONICITY_POWER = 4
SCORE_LOST_PENALTY = 200000
SCORE_MONOTONICITY_WEIGHT = 47
SCORE_SUM_WEIGHT = 11
SCORE_MERGES_WEIGHT = 700
SCORE_EMPTY_WEIGHT = 270

def find_best_move(board):
    """
    find the best move for the next turn.
    """

    move_args = [0,1,2,3]
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    res = max(result)
    bestmove = result.index(res)
    for m in move_args:
        print("move: %d score: %.4f" % (m, result[m]))
    return bestmove

def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    newboard = execute_move(move, board)

    if board_equals(board,newboard):
        return 0

    depth = 1
    prob = 1.0

    return score_tilechoose_node(depth, newboard, prob) + 1e-6

def score_tilechoose_node(depth, board, prob):
    """
    Score the leaf when the depth is reached or 
    when it has a low probability to reach this state to reduce the workload
    (example: in a board with many empty tiles and to get many 4 tiles in a row is very unlikely)
    It is needed when you have a high depth to reduce the workload a bit.
    
    If neither the depth is reached or the probability is too low, all possible states
    of the board will scored (recursively)
    """
    if depth > DEPTH_LIMIT or prob < LOW_PROBABILITY:
        return score_board(board)    
    res = 0.0   
    empty_positions = get_empty_positions(board)

    prob = prob / len(empty_positions)

    for position in empty_positions:
        y,x = position
        newboard = np.array(board)
        newboard[y][x]=2
        res += score_move_node(depth, newboard, prob*0.9)*0.9
        newboard[y][x]=4
        res += score_move_node(depth, newboard, prob*0.1)*0.1

    return res / len(empty_positions)
    
def score_move_node(depth, board, prob):
    """
    From the current board execute all 4 moves, score them and return the best board.
    """
    depth = depth + 1
    best = 0
    for move in range(4):
        newboard = execute_move(move, board)

        if not board_equals(board,newboard):
            best = max(best, score_tilechoose_node(depth, newboard, prob))

    return best
    
def score_board(board):
    """
	Get the score of the board.
      It take the number of empty fields, the value of the tiles, the possible merges and 
      if higher tiles are in the corner of the board into account
    """

    sumP,empty,merges = getHeuristics(board)
    mono = get_monotonicity(board) + get_monotonicity(np.transpose(board))
    merges2 = getHeuristics(np.transpose(board))[2]

    score = SCORE_LOST_PENALTY + SCORE_EMPTY_WEIGHT * empty * 2 + SCORE_MERGES_WEIGHT * (merges + merges2) - SCORE_MONOTONICITY_WEIGHT * mono - SCORE_SUM_WEIGHT * sumP * 2

    return score

def get_empty_positions(board):
    """
    Get the positions of the empty tiles on the board.
    """
    empty_positions = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty_positions.append((y,x))
    return empty_positions
    
def getHeuristics(b):
    """
    Get the heuristic for empty fields, possible merges and value of the tile.
    """
    board = board_log_2(b)
    sumP = 0
    empty = 0
    merges = 0
    prev = 0
    counter = 0
    for y in range(4):
        for x in range(4):
            rank = board[y][x]
            sumP += pow(rank, SCORE_SUM_POWER)
            if rank == 0:
                empty+=1
            else:
                if prev==rank:
                    counter+=1
                elif counter > 0:
                    merges += 1 + counter
                    counter = 0
                prev = rank
    if counter > 0:
        merges += 1 + counter
    return sumP,empty,merges
    
def get_monotonicity(b):
    """
    Get the monotonicity of the board. (When higher values are at the corner, the higher the score is)
    """
    board = board_log_2(b)
    mono = 0
    for y in range(4):
        mono_right = 0
        mono_left = 0
        for x in range(1,4):
            if board[y][x-1] > board[y][x]:
                mono_left += math.pow(board[y][x-1], SCORE_MONOTONICITY_POWER) - math.pow(board[y][x],SCORE_MONOTONICITY_POWER)
            else:
                mono_right += math.pow(board[y][x], SCORE_MONOTONICITY_POWER) - math.pow(board[y][x-1],SCORE_MONOTONICITY_POWER)
        mono += min(mono_right,mono_left)
    return mono

def board_log_2(board):
    """
	Return the board with his log2 value.
	Need to be sure that the score won't explode with high tiles.
    """
    logboard = []
    for y in range(4):
        logboard.append([])
        for x in range(4):
            val = 0
            if board[y][x] != 0:
                val = int(np.log2(board[y][x]))
            logboard[y].append(val)            
    return np.array(logboard)

def execute_move(move, board):
    """
    move and return the grid
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
		
def func_star(a_b):
    """
	Helper Method to split the programm in more processes.
	Needed to handle more than one parameter.
    """
    return score_toplevel_move (*a_b)

def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  
