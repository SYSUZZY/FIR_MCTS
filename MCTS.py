import numpy as np 
import pandas as pd 
import time
import random

from copy import deepcopy

from MCTSNode import MCTSNode
from Board import Board

max_workers=4

class MCTS(object):
    '''
    Use MCTS to choose a position
    '''

    def __init__(self, board, max_decision_time, max_simulation_times):
        self.board =  Board(board.board, board.n_in_row) # Chess board
        self.max_decision_time = max_decision_time
        self.max_simulation_times = max_simulation_times

        self.confident = 1.96 # the constant in UCT score function
        self.simulation_times = 0 # the times of simulation
        self.begin_time = time.time() # start the MCTS time

    
    def choose_position(self, last_player, last_position):
        '''
        Choose a position
        '''
        # One availables position left in the board
        if len(self.board.availables) == 1:
            return self.board.availables[0]
        root = MCTSNode(deepcopy(self.board), last_player, None, last_position)  # root is the current state of board
        position = self.monte_carlo_tree_search(root).position
        return position
        

    def monte_carlo_tree_search(self, root):
        '''
        MCTS process
        '''
        time_mcts = time.time()
        while self.resources_left():
            leaf = self.traverse(root)         # leaf is unvisited node
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
            self.simulation_times = root.visited_times
            # print(len(root.children))
        print('Simulation Times: {}'.format(self.simulation_times))
        print('Simulation time: {}'.format(time.time()-time_mcts))
        return root.get_best_child(self.uct)
    

    def backpropagate(self, node, result):
        '''
        Back propagate the result. 
        Update win times and visited times
        '''
        if node.player == result:
            node.win_times += 1
        node.visited_times += 1
        if node.parent == None:
            # The node is a root
            return
        self.backpropagate(node.parent, result)


    def rollout(self, node):
        '''
        Simulate a game up to game over
        '''
        current_state = deepcopy(node.board)
        player = node.player
        is_over, winner = current_state.check_game_result()
        while not is_over:
            player = -1*player
            position = self.rollout_policy(current_state)
            current_state.move(position, player)
            is_over, winner = current_state.check_game_result()
        return winner


    def is_terminal(self, node):
        '''
        Wether the node is terminal, which means someone win or no availables position.
        '''
        is_terminal, _ = node.board.check_game_result()
        return is_terminal


    def rollout_policy(self, board):
        '''
        Choose nearest positions first.
        '''
        # nearest_positions = []
        # if len(board.availables) > board.n_in_row:
        #     nearest_positions = self.find_nearest_position_first(board)
        # if len(nearest_positions):
        #     return random.choice(nearest_positions)
        # else:
        return random.choice(board.availables)

    def find_nearest_position_first(self, board):
        '''
        The method find nearest position sets
        '''
        
        nearest_positions = set() # create a set
        h, w = board.shape[0], board.shape[1]
        unavailables = board.unavailables
        for i, j in unavailables:
            # up down right left
            if i < h - 1:
                nearest_positions.add((i+1, j))
            if i > 0:
                nearest_positions.add((i-1, j))
            if j < w - 1:
                nearest_positions.add((i, j+1))
            if j > 0:
                nearest_positions.add((i, j-1))
            # diag
            if i < h - 1 and j < w - 1:
                nearest_positions.add((i+1, j+1))
            if i > 0 and j < w -1:
                nearest_positions.add((i-1, j+1))
            if i < h -1 and j > 0:
                nearest_positions.add((i+1, j-1))
            if i > 0 and j < w - 1:
                nearest_positions.add((i-1, j-1))
        # remove unavailables in nearest position
        nearest_positions = list(nearest_positions - set(unavailables))
        # check if nearest been used before
        for move in nearest_positions:
            if move in play: # TODO: need modified
                nearest_positions.remove(move)
        return nearest_positions


    def traverse(self, node):
        '''
        Traverse all the nodes and find the node that is not fully expeanded.

        (For the traverse function, to avoid using up too much time or resources, you may start considering only 
        a subset of children (e.g 10 children). Increase this number or by choosing this subset smartly later.)
        '''
        while not self.is_terminal(node):
            if not node.fully_expanded():
                return node.expand_child()
            else:
                node = node.get_best_child(self.uct)
        return node


    def resources_left(self):
        '''
        Wether the resources left
        '''
        isLeft = ((time.time() - self.begin_time) < self.max_decision_time) \
            and (self.simulation_times < self.max_simulation_times)
        return isLeft


    def uct(self, node):
        '''
        Score function
        '''
        return (node.win_times/node.visited_times) + self.confident*np.sqrt(np.log(node.parent.visited_times)/node.visited_times)


