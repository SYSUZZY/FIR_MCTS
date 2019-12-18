import numpy as np 
import pandas as pd 

class Board(object):

    def __init__(self, board, n_in_row):
        '''
        board: store the current chess board
        availables: read the available sites in the type of tuple (x,y)
        '''
        self.board = board
        self.n_in_row = n_in_row
        self.availables = [(i,j) for i in range(self.board.shape[0]) for j in range(self.board.shape[1]) if self.board[i][j] == 0]
        self.unavailables = [(i,j) for i in range(self.board.shape[0]) for j in range(self.board.shape[1]) if self.board[i][j] != 0]

    def move(self, position, player):
        '''
        input: position,player
        output: if move successfully, change the self.board,self.availables and return True;
                else, return False
        '''
        x,y = position
        if self.board[x,y] != 0:
            return False
        else:
            self.board[x,y] = player
            self.availables.remove((x,y))
            self.unavailables.append((x,y))
            return True
                       
    def check_a_list(self,ary,player):
        for i in range(len(ary)-4):
            count = 0
            j = i
            while ary[j] == player:
                if ary[j] == ary[j+1]:
                    count += 1
                    j += 1
                    if count == 4:
                        return True
                else:
                    break
        return False

    def check_game_result(self):
        '''
        Check the game result

        Return
        is_over: bool
        winner: if no winner, return None, else return winner
        '''
        # unavailables = [(i,j) for i in range(self.board.shape[0]) for j in range(self.board.shape[1]) if self.board[i][j] != 0]
        # print(unavailables)
        if(len(self.unavailables) < self.n_in_row + 2):
            return False, None

        board = self.board
        height = board.shape[0]
        width = board.shape[1]
        for chess in self.unavailables:
            row = chess[0]; col = chess[1]
            # Check in vertical
            if row <= height-self.n_in_row:
                if len(set([board[row+i][col] for i in range(self.n_in_row)])) == 1:
                    return True, board[row][col]
            # Check in horizontal
            if col <= width-self.n_in_row:
                if len(set([board[row][col+i] for i in range(self.n_in_row)])) == 1:
                    return True, board[row][col]
            # Check in diagonal
            if (row <= height-self.n_in_row) and (col <= width-self.n_in_row):
                if len(set([board[row+i][col+i] for i in range(self.n_in_row)])) == 1:
                    return True, board[row][col]
            # Check in anti-diagonal
            if (row <= height-self.n_in_row) and (col >= self.n_in_row-1):
                if len(set([board[row+i][col-i] for i in range(self.n_in_row)])) == 1:
                    return True, board[row][col]

        # No one wins till no vacancy in board
        if len(self.availables) == 0:
            return True, None

        return False, None

    def check_for_win(self,player):
        mat = self.board
        m,n = mat.shape
        mat2 = pd.DataFrame(mat)

        #horizontal        
        for i in range(m):
            ary = mat[i]
            check = self.check_a_list(ary,player)
            if check == True:
                return True

        #vertical
        for j in range(n):
            ary = np.array(mat2.loc[:,j])
            check = self.check_a_list(ary,player)
            if check == True:
                return True

        #diagonal
        for k in range(-(max(m,n)-5),max(m,n)-4):
            ary = [mat2.loc[i,j] for i in range(m) for j in range(n) if i - j == k]
            check = self.check_a_list(ary,player)
            if check == True:
                return True

        #anti-diagonal
        for l in range(4, max(m,n) *2 - 5):
            ary = [mat2.loc[i,j] for i in range(m) for j in range(n) if i + j == l]
            check = self.check_a_list(ary,player)
            if check == True:
                return True    

        return False
                
                
    def is_over(self):
        '''
        Wether the game is over
        '''
        if self.check_for_win(1) or self.check_for_win(-1) or (len(self.availables)==0):
            return True
        else:
            return False

    def game_result(self):
        '''
        return the winner
        black: 1   # human
        white: -1  # computer
        If no winner, return 0
        '''
        if self.check_for_win(1):
            return 1
        elif self.check_for_win(-1):
            return -1
        else:
            return 0
        
