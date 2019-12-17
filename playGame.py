import pygame
import numpy as np
import sys
import time

import pandas as pd

from MCTS import MCTS
from Board import Board

def update_by_man(event,mat):
    """
    This function detects the mouse click on the game window. Update the state matrix of the game. 
    input: 
        event:pygame event, which are either quit or mouse click)
        mat: 2D matrix represents the state of the game
    output:
        mat: updated matrix
    """
    global M
    done=False
    if event.type==pygame.QUIT:
        done=True
    if event.type==pygame.MOUSEBUTTONDOWN:
        (x,y)=event.pos
        row = round((y - 40) / 40)     
        col = round((x - 40) / 40)
        mat[row][col]=1
    return mat, done
def draw_board(screen):    
    """
    This function draws the board with lines.
    input: game windows
    output: none
    """
    global M
    #M=4
    d=int(560/(M-1))
    black_color = [0, 0, 0]
    board_color = [ 255, 222, 173 ]
    screen.fill(board_color)
    for h in range(0, M):
        pygame.draw.line(screen, black_color,[40, h * d+40], [600, 40+h * d], 1)
        pygame.draw.line(screen, black_color, [40+d*h, 40], [40+d*h, 600], 1)
def draw_stone(screen, mat):
    """
    This functions draws the stones according to the mat. It draws a black circle for matrix element 1(human),
    it draws a white circle for matrix element -1 (computer)
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none
    """
    black_color = [0, 0, 0]
    white_color = [255, 255, 255]
    M=len(mat)
    d=int(560/(M-1))
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j]==1:
                pos = [40+d * j, 40+d* i ]
                pygame.draw.circle(screen, black_color, pos, 18,0)
            elif mat[i][j]==-1:
                pos = [40+d* j , 40+d * i]
                pygame.draw.circle(screen, white_color, pos, 18,0)

def render(screen, mat):
    """
    Draw the updated game with lines and stones using function draw_board and draw_stone
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none        
    """
    
    draw_board(screen)
    draw_stone(screen, mat)
    pygame.display.update()

def draw_win_or_lose(screen,mat):    
    """
    This function draws the board with final result.
    input: game windows
    output: "win" or "lose" infomation
    """
    draw_board(screen)
    draw_stone(screen, mat)
    font = pygame.font.SysFont('timesnewromanttf',42)
    font_color = [139,69,19]
    if check_for_win(mat,1) == True:
        TextSurf = font.render('Game Over! Yon Win!',True,font_color)
    if check_for_win(mat,-1) == True:
        TextSurf = font.render('Game Over! Yon Lose!',True,font_color)        
    TextRect = TextSurf.get_rect()
    TextRect.center = (320,320)
    screen.blit(TextSurf,TextRect)
    pygame.display.update()

def check_a_list(ary,player):
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

def check_for_win(mat,player):
    
    m,n = mat.shape
    mat2 = pd.DataFrame(mat)
    #horizontal        
    for i in range(m):
        ary = mat[i]
        check = check_a_list(ary,player)
        if check == True:
            return True
    #vertical
    for j in range(n):
        ary = np.array(mat2.loc[:,j])
        check = check_a_list(ary,player)
        if check == True:
            return True
    #diagonal
    for k in range(-(max(m,n)-5),max(m,n)-4):
        ary = [mat2.loc[i,j] for i in range(m) for j in range(n) if i - j == k]
        check = check_a_list(ary,player)
        if check == True:
            return True
    #anti-diagonal
    for l in range(4, max(m,n) *2 - 5):
        ary = [mat2.loc[i,j] for i in range(m) for j in range(n) if i + j == l]
        check = check_a_list(ary,player)
        if check == True:
            return True    
    
    return False

def AI(mat, player, last_position):
    mcts = MCTS(Board(mat), 10)
    mat = mcts.choose_position(-1)
    return mat

def main():
    
    global M
    
    M=5
    
    pygame.init()
    screen=pygame.display.set_mode((640,640))
    pygame.display.set_caption('Five-in-a-Row')
    done=False
    mat=np.zeros((M,M))
    d=int(560/(M-1))
    draw_board(screen)
    pygame.display.update()

    
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                done=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                (x,y)=event.pos
                row = round((y - 40) / d)     
                col = round((x - 40) / d)
                mat[row][col] = 1
                render(screen, mat)
                done = check_for_win(mat,1)
                if not done:
                    "this is just temp move of computer for test!"
                    "need to substitude by the MontCalo tree research result"
                    # while True:
                    #     x = np.random.randint(0,M,1)[0]
                    #     y = np.random.randint(0,M,1)[0]
                    #     if mat[x-1,y-1] != 0:
                    #         continue
                    #     else:
                    #         mat[x-1,y-1] = -1
                    #         break
                    mat = AI(mat, -1, (row, col))
                    #time.sleep(2)
                    render(screen, mat)
                    done = check_for_win(mat,-1)

                               
                #get the next move from computer/MCTS
                # check for win or tie
                # print message if game finished
                # otherwise contibue
    
    draw_win_or_lose(screen,mat)

    pygame.quit()    
if __name__ == '__main__':
    main()