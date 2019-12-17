import numpy as np 
import pandas as pd 

class Board(object):

    def __init__(self, board):
        self.board = board  # store the current chess board
        self.available = [] # the available position

    
    def move(self, player):
        '''
        Randomly choose a position to put the chess
        '''
        pass


    def is_over(self):
        '''
        Wether the game is over
        '''
        pass

    def game_result(self):
        '''
        return the winner
        white: 1
        black: -1
        If no winner, return 0
        '''
        pass