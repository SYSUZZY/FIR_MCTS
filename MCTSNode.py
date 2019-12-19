import random
from queue import Queue
from copy import deepcopy
from Board import Board
import Config
from Sprite import Sprite

class MCTSNode(object):
    '''
    MCTSNode in the MCT
    '''
    
    def __init__(self, board, player, parent, position):
        self.board = board
        self.player = player
        self.parent = parent
        self.position = position

        self.children = []

        # Max children number
        self.max_expend_num = Config.CHILDREN_NUM
        if len(board.availables) < self.max_expend_num:
            self.max_expend_num = len(board.availables)

        self.win_times = 0
        self.visited_times = 0

        self._untried_actions = None
        self._untried_far_actions = []
    

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            pattern_children = list((set(self.board.unavailables)|set(self.find_naive_pattern()))-set(self.board.unavailables))
            nearest_children = list(set(self.find_nearest_position_first()) - set(pattern_children))
            available_children = list(set(deepcopy(self.board.availables)) - set(pattern_children) - set(nearest_children))
            self._untried_actions = pattern_children + nearest_children + available_children

        return self._untried_actions
        

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
            player = Sprite.change_player(self.player)
            state = deepcopy(self.board.state)
            position = self.untried_actions.pop(0)
            state = Board(state, self.board.n_in_row)

            state.move(position, player)
            new_child = MCTSNode(state, player, self, position)
            self.children.append(new_child)
            return new_child
        else:
            print('Reach the maximum children number!')
            return None
    

    def find_naive_pattern(self):
        '''
        Find the pattern in this state
        Choose the best position in the availables
        '''
        children_list = self.board.find_position_by_pattern()
        return children_list


    def find_nearest_position_first(self):
        '''
        The method find nearest position sets
        '''

        nearest_positions = set() # create a set
        h, w = self.board.state.shape[0], self.board.state.shape[1]
        unavailables = self.board.unavailables
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
            if i > 0 and j > 0:
                nearest_positions.add((i-1, j-1))
        # remove unavailables in nearest position
        nearest_positions = list(set(nearest_positions) - set(unavailables))
        return nearest_positions


    def show_MCTS(self):
        '''
        Show the node of tree
        (For Debug)
        '''
        que = Queue()
        que.put(self)
        count = 0
        while not que.empty():
            if count > 15:
                break
            node = que.get()
            print(node.board.state)
            print(node.player)
            print(node.parent)
            print(node.position)
            print(node.win_times)
            print(node.visited_times)
            if len(node.children) != 0:
                for child in node.children:
                    que.put(child)
            count += 1
