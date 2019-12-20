import numpy as np 
import pandas as pd 

class Board(object):

    def __init__(self, state, n_in_row):
        '''
        state: store the current chess state
        availables: read the available sites in the type of tuple (x,y)
        '''
        self.state = state
        self.n_in_row = n_in_row
        self.availables = [(i,j) for i in range(self.state.shape[0]) for j in range(self.state.shape[1]) if self.state[i][j] == 0]
        self.unavailables = [(i,j) for i in range(self.state.shape[0]) for j in range(self.state.shape[1]) if self.state[i][j] != 0]


    def move(self, position, player):
        '''
        input: position, player
        output: if move successfully, change the self.state,self.availables and return True;
                else, return False
        '''
        x,y = position
        if self.state[x,y] != 0:
            return False
        else:
            self.state[x,y] = player
            self.availables.remove((x,y))
            self.unavailables.append((x,y))
            return True


    def check_game_result(self):
        '''
        Check the game result

        output: is_over: bool
                winner: if no winner, return None, else return winner
        '''
        # unavailables = [(i,j) for i in range(self.state.shape[0]) for j in range(self.state.shape[1]) if self.state[i][j] != 0]
        # print(unavailables)
        if(len(self.unavailables) < self.n_in_row + 2):
            return False, None

        state = self.state
        height = state.shape[0]
        width = state.shape[1]
        for chess in self.unavailables:
            row = chess[0]; col = chess[1]
            # Check in vertical
            if row <= height-self.n_in_row:
                if abs(sum([state[row+i][col] for i in range(self.n_in_row)])) == self.n_in_row:
                    return True, state[row][col]
            # Check in horizontal
            if col <= width-self.n_in_row:
                if abs(sum([state[row][col+i] for i in range(self.n_in_row)])) == self.n_in_row:
                    return True, state[row][col]
            # Check in diagonal
            if (row <= height-self.n_in_row) and (col <= width-self.n_in_row):
                if abs(sum([state[row+i][col+i] for i in range(self.n_in_row)])) == self.n_in_row:
                    return True, state[row][col]
            # Check in anti-diagonal
            if (row <= height-self.n_in_row) and (col >= self.n_in_row-1):
                if abs(sum([state[row+i][col-i] for i in range(self.n_in_row)])) == self.n_in_row:
                    return True, state[row][col]

        # No one wins till no vacancy in state
        if len(self.availables) == 0:
            return True, None

        return False, None


    def find_position_by_pattern(self):
        '''
        Find the pattern in this state
        Choose the best position in the availables
        '''
        children_list = []
        
        if(len(self.unavailables) < self.n_in_row):
            return children_list

        state = self.state
        height = state.shape[0]
        width  = state.shape[1]
        for chess in self.unavailables:
            row = chess[0]; col = chess[1]
            # Check in vertical
            if (row >= 1) and (row <= height-self.n_in_row+1):
                pattern_5 = [state[row-1+i][col] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    pattern_3 = [state[row+i][col] for i in range(self.n_in_row-2)]
                    empty_in_pattern = self.__find_position_by_pattern(pattern_5, pattern_3)
                    for empty_index in empty_in_pattern:
                        children_list.append((row-1+empty_index, col))
            if (row >= 0) and (row <= height-self.n_in_row):
                pattern_5 = [state[row+i][col] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    if (len(set(pattern_5)) == 2) and (abs(sum(pattern_5)) == self.n_in_row-1):
                        children_list.append((row+4, col))

            # Check in horizontal
            if (col >= 1) and (col <= width-self.n_in_row+1):
                pattern_5 = [state[row][col-1+i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    pattern_3 = [state[row][col+i] for i in range(self.n_in_row-2)]
                    empty_in_pattern = self.__find_position_by_pattern(pattern_5, pattern_3)
                    for empty_index in empty_in_pattern:
                        children_list.append((row, col-1+empty_index))
            if (col >= 0) and (col <= width-self.n_in_row):
                pattern_5 = [state[row][col+i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    if (len(set(pattern_5)) == 2) and (abs(sum(pattern_5)) == self.n_in_row-1):
                        children_list.append((row, col+4))

            # Check in diagonal
            if (row >= 1) and (row <= height-self.n_in_row+1) and (col >= 1) and (col <= width-self.n_in_row+1):
                pattern_5 = [state[row-1+i][col-1+i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    pattern_3 = [state[row+i][col+i] for i in range(self.n_in_row-2)]
                    empty_in_pattern = self.__find_position_by_pattern(pattern_5, pattern_3)
                    for empty_index in empty_in_pattern:
                        children_list.append((row-1+empty_index, col-1+empty_index))
            if (col >= 0) and (col <= width-self.n_in_row) and (row >= 0) and (row <= height-self.n_in_row):
                pattern_5 = [state[row+i][col+i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    if (len(set(pattern_5)) == 2) and (abs(sum(pattern_5)) == self.n_in_row-1):
                        children_list.append((row+4, col+4))

            # Check in anti-diagonal
            if (row >= 1) and (row <= height-self.n_in_row+1) and (col >= self.n_in_row-2) and (col <= width-2):
                pattern_5 = [state[row-1+i][col+1-i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    pattern_3 = [state[row+i][col-i] for i in range(self.n_in_row-2)]
                    empty_in_pattern = self.__find_position_by_pattern(pattern_5, pattern_3)
                    for empty_index in empty_in_pattern:
                        children_list.append((row-1+empty_index, col+1-empty_index))
            if (col >= self.n_in_row-1) and (col <= width-1) and (row >= 0) and (row <= height-self.n_in_row):
                pattern_5 = [state[row+i][col-i] for i in range(self.n_in_row)]
                if 0 in pattern_5:
                    if (len(set(pattern_5)) == 2) and (abs(sum(pattern_5)) == self.n_in_row-1):
                        children_list.append((row+4, col-4))
        return list(set(children_list))


    def __find_position_by_pattern(self, pattern_5, pattern_3):
        pattern_sum = sum(pattern_5)
        pattern_set = len(set(pattern_5))
        empty_in_pattern = []
        if (abs(pattern_sum) == self.n_in_row-1) and (pattern_set == 2):
            empty_in_pattern.append(pattern_5.index(0))
        elif (abs(pattern_sum) == self.n_in_row-2) and (pattern_set == 2):
            empty_in_pattern.append(pattern_5.index(0))
            empty_in_pattern.append(pattern_5.index(0, 1))
        elif (abs(pattern_sum) == self.n_in_row-3) and (len(set(pattern_3)) == 1) and (list(set(pattern_3)) != 0):
            empty_in_pattern.append(pattern_5.index(0))
        return list(set(empty_in_pattern))