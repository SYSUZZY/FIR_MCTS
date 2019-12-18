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

def draw_win_or_lose(screen,board):    
    """
    This function draws the board with final result.
    input: game windows
    output: "win" or "lose" infomation
    """
    draw_board(screen)
    draw_stone(screen, board.board)
    font = pygame.font.SysFont('timesnewromanttf',42)
    font_color = [139,69,19]
    if board.game_result() == 1:
        TextSurf = font.render('Game Over! Yon Win!',True,font_color)
    elif board.game_result() == 0:
        TextSurf = font.render('Game Over! Yon Lose!',True,font_color)   
    else:
        TextSurf = font.render('Game Over! A Tie!',True,font_color)  
    TextRect = TextSurf.get_rect()
    TextRect.center = (320,320)
    screen.blit(TextSurf,TextRect)
    pygame.display.update()


def AI(board, last_player, last_position):
    mcts = MCTS(board, 5, 1000)
    position = mcts.choose_position(last_player, last_position)
    return position

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

    # Board
    board = Board(mat, 5)    
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                done=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                (x,y)=event.pos
                row = round((y - 40) / d)     
                col = round((x - 40) / d)
                if not board.move((row, col), 1):
                    print('The position is not available.')
                    break
                render(screen, board.board)
                done = board.check_for_win(1)
                if not done:
                    AI_position = AI(board, 1, (row, col))
                    board.move(AI_position, -1)
                    render(screen, board.board)
                    done = board.check_for_win(-1)
    
    draw_win_or_lose(screen,board)

    pygame.quit()    
if __name__ == '__main__':
    main()
