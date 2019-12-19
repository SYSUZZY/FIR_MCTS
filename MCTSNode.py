import random
from queue import Queue
from copy import deepcopy
from Board import Board
import Config

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
            pattern_children = self.find_naive_pattern()
            nearest_children = list(set(self.find_nearest_position_first()) - set(pattern_children))
            available_children = list(set(deepcopy(self.board.availables)) - set(pattern_children) - set(nearest_children))
            random.shuffle(available_children)
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
            # a = deepcopy(self.board.board)
            player = -self.player                 # change player

            state_mat = deepcopy(self.board.board)
            print(self.untried_actions)
            position = self.untried_actions.pop(0) # random choose an availables position
            state = Board(state_mat, self.board.n_in_row)

            state.move(position, player)
            # state = Board(state.board, state.n_in_row)
            new_child = MCTSNode(state, player, self, position)
            self.children.append(new_child)
            # b = deepcopy(self.board.board)
            # if not (a == b).all():
            #     print("change")
            return new_child
        else:
            print('Reach the maximum children number!')
            return None
    
    def find_naive_pattern(self):
        op = -1 * self.player
        agent = self.player
        board = self.board.board
        # chosen child
        children_list = []
		# desired pattern
        fourInRow = ([op, op, op, op, 0], [0, op, op, op, op])
        threeInRow = ([0, op, op, op, 0], [agent, op, op, op, 0], [0, op, op, op, agent])
        for i in range(len(board)):
            for j in range(len(board)):
                allPattern = ( [board[p][j] if p >= 0 and p < len(board) else -2 for p in range(i-4, i+1)], \
								[board[p][j] if p >= 0 and p < len(board) else -2 for p in range(i, i+5)], \
								[board[i][p] if p >= 0 and p < len(board) else -2 for p in range(j-4, j+1)], \
								[board[i][p] if p >= 0 and p < len(board) else -2 for p in range(j, j+5)], \
								[board[i+p][j+p] if i + p >= 0 and i + p < len(board) and j + p >= 0 and j + p < len(board) else -2 for p in range(-4, 0)], \
								[board[i+p][j+p] if i + p >= 0 and i + p < len(board) and j + p >= 0 and j + p < len(board) else -2 for p in range(0, 5)] 
                                    )
                for pattern in allPattern:
                    if pattern in fourInRow and board[i][j] == 0:
                        children_list = [(i, j)] + children_list
                    elif pattern in threeInRow and board[i][j] == 0:
                        children_list.append((i, j))
        return children_list

    def find_nearest_position_first(self):
        '''
        The method find nearest position sets
        '''

        nearest_positions = set() # create a set
        h, w = self.board.board.shape[0], self.board.board.shape[1]
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
        que = Queue()
        que.put(self)
        count = 0
        while not que.empty():
            if count > 15:
                break
            node = que.get()
            print(node.board.board)
            print(node.player)
            print(node.parent)
            print(node.position)
            print(node.win_times)
            print(node.visited_times)
            if len(node.children) != 0:
                for child in node.children:
                    que.put(child)
            count += 1


