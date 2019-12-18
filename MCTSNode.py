import random
from copy import deepcopy

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

        self.max_expend_num = 10  # A node has 10 children or available position num at most
        if len(board.availables) > self.max_expend_num:
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
            player = -self.player                 # change player

            state = deepcopy(self.board)
            position = self.untried_actions.pop() # random choose an availables position
            state.move(position, player)

            new_child = MCTSNode(state, player, self, position)
            self.children.append(new_child)
            return new_child
        else:
            print('Reach the maximum children number!')
            return None
    

    def different_position(self, availables):
        '''
        Find a different position with other children
        '''
        if len(self.children) == 0:
            # parent has no child
            return random.choice(availables)
        
        # parent has child
        not_find = True
        while not_find:
            position = random.choice(availables)
            not_find = False
            for child in self.children:
                if position == child.position:
                    not_find = True
                    break
        return position