import numpy as np 
import pandas as pd 
import time
import random

from copy import deepcopy

from MCTSNode import MCTSNode

class MCTS(object):
    '''
    Use MCTS to choose a position
    '''

    def __init__(self, board, max_decision_time, max_simulation_times):
        self.board = board  # Chess board
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
        while self.resources_left():
            leaf = self.traverse(root)         # leaf is unvisited node
            simulation_result = self.rollout(deepcopy(leaf))
            self.backpropagate(leaf, simulation_result)
            self.simulation_times = root.visited_times
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
        current_state = node.board
        player = node.player
        while not current_state.is_over():
            player = -1*player
            position = self.rollout_policy(current_state)
            current_state.move(position, player)
        return current_state.game_result()


    def is_terminal(self, node):
        '''
        Wether the node is terminal, which means someone win or no availables position.
        '''
        return node.board.is_over()


    def rollout_policy(self, board):
        '''
        Random put a position
        '''
        return random.choice(board.availables)


    def traverse(self, node):
        '''
        Traverse all the nodes and find the node that is not fully expeanded.

        (For the traverse function, to avoid using up too much time or resources, you may start considering only 
        a subset of children (e.g 10 children). Increase this number or by choosing this subset smartly later.)
        '''
        while node.fully_expanded():
            node = node.get_best_child(self.uct)
        # node is not fully expanded
        if self.is_terminal(node):
            # if the node is terminal
            unvisited_node = node
        else:
            # if the node is no a terminal
            unvisited_node = node.expand_child()
        return unvisited_node


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
        return (node.win_times/node.visited_times) + self.confident*np.sqrt(2*np.log(node.parent.visited_times)/node.visited_times)