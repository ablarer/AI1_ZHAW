import game
import sys
import numpy as np

# Author:				chrn 
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.
# Highscore:                Score 12128, highest tile 1024

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    
    bestmove = -1
    bestscore = 0
    
    for move in range(4):
        res = get_score(move,board)
        print(f'Move: {move} Score: {res}')
        if res > bestscore:
            bestmove = move
            bestscore = res
        
    print (bestmove)
    return bestmove
    
def get_score(move,board):
    '''
        Calculate the score of the move on the current board.
    '''
    newboard = execute_move(move,board)
    if board_equals(board,newboard):
        return 0
    nr_empty = len(get_empty_positions(newboard))
    merge_score = get_merge_score(newboard,get_merge_tiles(newboard))
    
    # Magic numbers, performed best in the tested numbers. 
    # But other numbers could perform better
    return nr_empty * 100 + merge_score * 20
    
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()    

def get_merge_score(board,merge_tiles):
    """
        Dependent of the value of the tile it give you a higher score.
    """
    score = 0
    for tile in merge_tiles:
        score += np.log2(board[tile[0]][tile[1]])
    return score
    
def get_merge_tiles(board):
    """
        Get the position of all tiles which which has next to them a tile
        with the same value. A pair of tiles with same value only one of the
        tile is in the list.
        And no tile is in the list twice.
    """
    merge_tiles = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                continue
            if x < 3:
                if board[y][x] == board[y][x+1]:
                    merge_tiles.append((y,x))
                    continue
            if y < 3:
                if board[y][x] == board[y+1][x]:
                    merge_tiles.append((y,x))
    return merge_tiles
    
def get_empty_positions(board):
    '''
        Get all empty positions on the board.
    '''
    empty_positions = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty_positions.append((y,x))
    return empty_positions
    

def execute_move(move, board):
    """
    move and return the grid
    """
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