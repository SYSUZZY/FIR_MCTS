import numpy as np 
from queue import Queue

import pygame
import multiprocessing
from copy import deepcopy

import Config
from AI import AI
from Board import Board
from Player import Player

class GameEngine(object):
    '''
    Game Engine
    '''

    def __init__(self):
        '''
        Game Engine Setting
        '''
        self.board_size = Config.board_size
        self.screen = None
        self.is_quit = False
        self.mouse_position = None
        self.clock = pygame.time.Clock()

        '''
        Sprite
        '''
        self.board = Board(np.zeros((Config.board_size, Config.board_size)), Config.n_in_row)
        self.human = Player(Config.HUMAN)
        self.ai = AI(Config.AI)

        '''
        Game
        '''
        self.turn = Config.HUMAN
        self.signal = multiprocessing.Queue(1)
        self.ai_process = None
        self.check_board = False
        self.is_over = False
        self.winner = None

        self.game_initialize()


    def game_initialize(self):
        '''
        initialize pygame
        '''
        pygame.init()
        self.is_quit = False
        self.screen = pygame.display.set_mode(Config.windows_size)
        pygame.display.set_caption('Five-in-a-Row')
        self.draw_board(self.screen)
        pygame.display.update()
    

    def start_game(self):
        '''
        Game Start
        '''
        while not self.is_quit:
            # Events listener
            self.__events_handler()
            # Player turn detect
            self.__player_turn_detect()
            # Update sprites
            self.__update_sprites()
            # Render
            self.__render()

    def __events_handler(self):
        '''
        Handle the events from IO
        '''
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.is_quit = True
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = event.pos


    def __player_turn_detect(self):
        if self.turn == self.human.id:
            pass
            # print('Human turn')
        else:
            # print('AI turn')
            pass


    def __update_sprites(self):
        '''
        Update the state of sprites
        '''
        if self.turn == self.human.id and self.mouse_position:
            move_success, err_msg = self.update_human()
            if move_success:
                self.turn = Config.AI
                self.check_board = True
            else:
                print(err_msg)
        elif self.turn == self.ai.id:
            if not self.signal.empty():
                if self.signal.get() == Config.AI_THREAD_DONE:
                    # Initialize the ai process
                    print('AI process end!')
                    self.ai.position = self.signal.get() # pass the position
                    self.ai_process.terminate()
                    self.ai_process.join()
                    self.ai_process = None
                    self.update_AI()
                    self.turn = Config.HUMAN
                    self.check_board = True
            else:
                if not self.ai_process:
                    print('AI process start!')
                    self.signal.put(Config.AI_THREAD_WORK)
                    self.ai_process = multiprocessing.Process(target = self.ai.choose_position, 
                        args=(deepcopy(self.board), self.human.id, self.human.last_position, self.signal,))
                    self.ai_process.start()

        if self.check_board:
            self.check_game_result()


    def check_game_result(self):
        '''
        Check the game result
        '''
        is_over, winner = self.board.check_game_result()
        if is_over and self.turn:
            self.is_over = is_over
            self.winner = winner
            self.turn = None

    
    def update_AI(self, signal=None):
        '''
        Run the MCTS in another thread
        '''
        if self.ai_process:
            pass
            # self.ai.choose_position(deepcopy(self.board), self.human.id, self.human.last_position, signal)
        else:
            self.board.move(self.ai.position, self.ai.id)


    def update_human(self):
        """
        This function detects the mouse click on the game window. Update the state matrix of the game. 
        """
        # Add a position detect later #
        move_success = False
        err_msg = 'The position is not available.'
        if self.mouse_position:
            (x,y) = self.mouse_position
            d = int(560/(self.board_size-1))
            row = round((y - 40) / d)
            col = round((x - 40) / d)
            move_success = self.board.move((row, col), self.human.id)
            if move_success:
                self.human.last_position = (row, col)
            self.mouse_position = None

        return move_success, err_msg


    def draw_board(self, screen):    
        """
        This function draws the board with lines.
        input: game windows
        output: none
        """
        d = int(560/(self.board_size-1))
        black_color = [0, 0, 0]
        board_color = [255, 222, 173]
        screen.fill(board_color)
        
        for h in range(0, self.board_size):
            pygame.draw.line(screen, black_color, [40, h * d+40], [600, 40+h * d], 1)
            pygame.draw.line(screen, black_color, [40+d*h, 40], [40+d*h, 600], 1)


    def draw_stone(self, screen, mat):
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
        d = int(560/(self.board_size-1))
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if mat[i][j] == 1:
                    pos = [40+d*j, 40+d*i]
                    pygame.draw.circle(screen, black_color, pos, 18,0)
                elif mat[i][j] == -1:
                    pos = [40+d*j, 40+d*i]
                    pygame.draw.circle(screen, white_color, pos, 18,0)


    def __render(self):
        """
        Draw the updated game with lines and stones using function draw_board and draw_stone
        input:
            screen: game window, onto which the stones are drawn
            mat: 2D matrix representing the game state
        output:
            none
        """
        self.clock.tick(10)
        self.draw_board(self.screen)
        self.draw_stone(self.screen, self.board.state)
        if self.is_over:
            self.draw_win_or_lose(self.screen)
        pygame.display.update()


    def draw_win_or_lose(self, screen):
        """
        This function draws the board with final result.
        input: game windows
        output: "win" or "lose" infomation
        """
        font = pygame.font.SysFont('timesnewromanttf',42)
        font_color = [139,69,19]
        if self.winner == Config.HUMAN:
            text_surf = font.render('Game Over! Yon Win!',True,font_color)
        elif self.winner == Config.AI:
            text_surf = font.render('Game Over! Yon Lose!',True,font_color)
        else:
            text_surf = font.render('Game Over! A Tie!',True,font_color)
        text_rect = text_surf.get_rect()
        text_rect.center = (320,320)
        screen.blit(text_surf, text_rect)