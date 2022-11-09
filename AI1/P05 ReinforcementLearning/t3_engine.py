# -*- coding: utf-8 -*-
"""
Game engine for Tic-Tac-Toe

Autor: stdm
Creation: Feb 14, 2018


Description of the game state:
------------------------------
    
The fields in the board are addressed with single numbers in the following way:

   1|2|3
   -----
   4|5|6
   -----
   7|8|9

A board is encoded as a string of single characters of length 9, for example:
    
   '   XO    '
    123456789 (<- field numbers)

where empty fields are marked by ' ', Xs are marked by 'X' and Os by 'O'. In
the example, there's a X on field 4 and an O on field 5 (the middle position).

The complete game state equals the current board configuration because the 
question who's turn it is can be deduced from the number of empty fields: it is 
X's turn iif the number of free fields is 9/7/5/3/1 -> uneven; otherwise it is 
O's turn.
"""

def insert_symbol(board, symbol, field):
    """
    Return a new BOARD by inserting the character SYMBOL at the index position 
    FIELD-1.
    """
    idx = field-1
    return board[:idx] + symbol + board[idx+1:]


def make_move(board, field, symbol):
    """
    make_move(board, field, symbol) executes the move indictaed by its 
    parameters:
        The SYMBOL ('X' or 'O') is put into the indicated FIELD (1-9) of a new 
        BOARD (encoding: see above), if this is a valid move.
        The function returns the new BOARD if the move is valid; '' otherwise.
    """
    i_field = int(field)
    if i_field>0 and i_field<10:
        if symbol=='X' or symbol=='O':
            if board[i_field-1] == ' ': #valid move if field is still empty
                return insert_symbol(board, symbol, i_field)
    return '' #something was invalid


def evaluate(board):
    """
    evluate(board) indicates if a game is over, and if so, who has won. To 
    simplify things, a game is only over when one either player has won (3 in a 
    row / column / diagonal), or the board is full (in this case it is draw).
    evaluate(board) returns a tupel (OVER?, WHO_WON, REWARD):
        The first entry indicates (TRUE/FALSE) if the game has reached a final 
        state.
        The second entry indicates who one (either 'X' or 'O').
        The third entry indicates who has won (from X's perspective, if the 
        first entry is TRUE): +1 indicates a win for X, -1 a win for O, an 0 a 
        draw
    """
    #check rows:
    for i in range(3):    
        if board[i*3]==board[i*3+1] and board[i*3]==board[i*3+2] and board[i*3]!=' ':
            if board[i*3]=='X':
                return (True, 'X', +1)
            else:
                return (True, 'O', -1)
            
    #check cols:
    for i in range(3):    
        if board[i]==board[i+3] and board[i]==board[i+6] and board[i]!=' ':
            if board[i]=='X':
                return (True, 'X', +1)
            else:
                return (True, 'O', -1)
            
    #check diagonals:
    if board[0]==board[4] and board[0]==board[8] and board[0]!=' ': #down diag
        if board[0]=='X':
            return (True, 'X', +1)
        else:
            return (True, 'O', -1)                
    if board[6]==board[4] and board[6]==board[2] and board[6]!=' ': #up diag
        if board[6]=='X':
            return (True, 'X', +1)
        else:
            return (True, 'O', -1)
        
    #check draw (board full):
    if count_symbol(board, ' ') == 0:
        return (True, 'Nobody', 0)
    
    #oterhwise: game not over
    return (False, 'Nobody', 0)


def count_symbol(board, symbol):
    """
    Returns the number SYMBOLs on the BOARD
    """
    count = 0
    for i in range(9):
        if board[i]==symbol:
            count = count+1
    return count


def whos_turn(board):
    """
    Returns the SYMBOL of the player who's turn it is: it is X's turn iif the 
    number of free fields is 9/7/5/3/1 -> uneven; otherwise it is O's turn.
    """
    free_fields = count_symbol(board, ' ')
    if free_fields%2 > 0: #i.e., free_field is uneven
        return 'X'
    else:
        return 'O'

    
def get_initial_board():
    """
    Returns an empty BOARD so that a user does not need to have knowledge of 
    its encoding.
    """
    return '         '    


def print_board(board, with_numbers=True):
    """
    Pretty-prints the BOARD in the way described above (Description of the game 
    state). If IF_NUMBERS == True, the emtpy fields are printed with their 
    respective field numbers.
    """
    print()
    for i in range(3):
        if with_numbers:
            #replace ' ' by field-number
            print((str(i*3+1) if board[i*3]==' ' else board[i*3]) + '|' + (str(i*3+2) if board[i*3+1]==' ' else board[i*3+1]) + '|' + (str(i*3+3) if board[i*3+2]==' ' else board[i*3+2]))
        else:
            print(board[i*3] + '|' + board[i*3+1] + '|' + board[i*3+2])
        if i<2:
            print('-----')
    return


def print_help():
    """
    Print a help text for a potential user as how to address fields in the 
    board.
    """
    print("The fields in the board are addressed with single numbers in the following way:")
    print("1|2|3")
    print("-----")
    print("4|5|6")
    print("-----")
    print("7|8|9")
    print()

    return
