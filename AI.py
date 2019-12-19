import Config
import threading
from MCTS import MCTS
from Sprite import Sprite


class AI(Sprite):

    def __init__(self, id):
        Sprite.__init__(self, id)
        self.position = None


    def choose_position(self, cur_board, player_id, last_position, signal):
        '''
        Use the MCTS to find a position
        Used for multiprocessing
        '''
        print('Start:{}'.format(signal.get()))
        mcts = MCTS(cur_board, Config.THINK_TIME, Config.SIMULATION_TIMES)
        position = mcts.choose_position(player_id, last_position)
        signal.put(Config.AI_THREAD_DONE)
        signal.put(position)