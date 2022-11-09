# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe controller TEMPLATE

Autor: stdm
Creation: Feb 14, 2018

"""

import random
#TODO: import t3_agent as agent # <- implement and include your own learning agent
import t3_engine as engine


#Some definitions to configure the behaviour of this controller
training_mode = False


#control both training and playing
def main():
    random.seed()
    
    print('Welcome to the Tic-Tac-Toe self-play RL agent environment.')
    engine.print_help()

    #train a RL agent by self-play
    if training_mode:
        print('TODO')
            
    #apply a trained RL agent in a game aghainst a human
    else: #training_mode==False
        board = engine.get_initial_board()
        model = agent.load_model(model_file_name) # <- API to fulfill by own agent implementation: load a trained model from a file (the model can have any format, as only your agent is going to use it internally)
        print('You are player O, the computer starts.')
        
        while True:
            turn = engine.whos_turn(board)
            if turn=='X': #get the agent's input, make the respective move                
                field = agent.get_best_action(board, model, turn) # <- API to fulfill by own agent implementation: return the best possible move (field# 1-9, according to learnt model) in the given state; the board has a format specified in t3_engine.py
                board = engine.make_move(board, field, turn)
                assert(board!='')
            else: #get player's input (until valid) and make the respective move
                while True: 
                    field = input("Which field to set? ")
                    board = engine.make_move(board, field, turn)
                    if board!='':
                        break
            
            #print new state, evaluate game
            print('Game after ' + turn + "'s move: ")
            engine.print_board(board, False)
            game_over, who_won, reward = engine.evaluate(board)
            
            if game_over:
                print('The game is over. ' + who_won + ' won.')
                break

    return # end of main()


# start the script if executed directly    
if __name__ == '__main__':
    
    main()
