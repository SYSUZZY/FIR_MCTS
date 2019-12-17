import numpy as np 
import pandas as pd 
import time
import random

from copy import deepcopy

class Node(object):
    '''
    Node in the MCT
    '''
    
    def __init__(self, board, player, parent, position):
        self.board = board
        self.player = player
        self.parent = parent
        self.position = position

        self.children = []

        self.max_expend_num = 5  # A node has 5 children at most
        self.win_times = 0
        self.visited_times = 0
        

    def fully_expanded(self):
        '''
        Wether the node is fully expanded
        '''
        return len(self.children) == self.max_expend_num


    def get_best_child(self, score_method):
        '''
        Score all the children by the score method
        Return a best one
        '''
        if len(self.children) == 0:
            print('The node has no child!')
            return None
        children_scores = [(child, score_method(child)) for child in self.children]
        best_child = max(children_scores, key=lambda x: x[1])[0]
        return best_child

    
    def expand_child(self):
        '''
        If the node is not a fully expanded node, add a child.
        The child is a player node different from the parent, and it has a different board
        The child put a chess in a random position
        '''
        if len(self.children) < self.max_expend_num:
            new_board = deepcopy(self.board)
            player = -self.player # change player
            position = random.choice(new_board.availables) # random choose an availables position
            new_board.move(position, player)
            new_child = Node(new_board, player, self, position)
            self.children.append(new_child)
            return new_child
        else:
            print('Reach the maximum children number!')
            return None


class MCTS(object):
    '''
    Use MCTS to choose a position
    '''

    def __init__(self, board, max_decision_time):
        self.board = board  # Chess board
        self.max_decision_time = max_decision_time
        self.confident = 1.96 # the constant in UCT score function
        self.simulation_times = 0 # the times of simulation

    
    def choose_position(self, cur_player, cur_position):
        '''
        Choose a position
        '''
        # One availables position left in the board
        if len(self.board.availables) == 1:
            return self.board.availables[0]

        root = Node(deepcopy(self.board), cur_player, None, cur_position)  # root is the current state of board
        position = self.monte_carlo_tree_search(root).position
        return position
        

    def monte_carlo_tree_search(self, root):
        '''
        MCTS process
        '''
        begin_time = time.time()
        while self.resources_left(begin_time):
            print('simulation times:{}'.format(self.simulation_times))
            leaf = self.traverse(root)         # leaf is unvisited node
            simulation_result = self.rollout(deepcopy(leaf))
            self.backpropagate(leaf, simulation_result)
            self.simulation_times += 1
        return root.get_best_child(self.uct)
    

    def backpropagate(self, node, result):
        '''
        Back propagate the result. 
        Update win times and visited times
        '''
        if node.parent == None:
            # The node is a root
            return
        if node.player == result:
            node.win_times += 1
        node.visited_times += 1
        self.backpropagate(node.parent, result)
        

    def rollout(self, node):
        '''
        Simulate a game up to game over
        '''
        while not self.is_terminal(node):
            node = self.rollout_policy(node)
        return node.board.game_result()


    def is_terminal(self, node):
        '''
        Wether the node is terminal, which means someone win or no availables position.
        '''
        terminal_flag = False
        if len(node.board.availables) == 0:
            terminal_flag = True
        elif node.board.is_over():
            terminal_flag = True
        return terminal_flag

    def rollout_policy(self, node):
        '''
        Random put a position
        '''
        return node.expand_child()


    def traverse(self, node):
        '''
        Traverse all the nodes and find the node that is not fully expeanded.

        (For the traverse function, to avoid using up too much time or resources, you may start considering only 
        a subset of children (e.g 5 children). Increase this number or by choosing this subset smartly later.)
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


    def resources_left(self, begin_time):
        '''
        Wether the resources left
        '''
        isLeft = (time.time() - begin_time) < self.max_decision_time
        return isLeft


    def uct(self, node):
        '''
        Score function
        '''
        return (node.win_times/node.visited_times) + self.confident*np.sqrt(np.log(self.simulation_times)/node.visited_times)