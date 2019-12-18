import random
from queue import Queue
from copy import deepcopy
from Board import Board

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

        self.max_expend_num = 10 # A node has 10 children or available position num at most
        if len(board.availables) < self.max_expend_num:
            self.max_expend_num = len(board.availables)

        self.win_times = 0
        self.visited_times = 0

        self._untried_actions = None
    

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.board.availables
        random.shuffle(self._untried_actions)
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
            position = self.untried_actions.pop() # random choose an availables position
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


