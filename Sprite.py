import Config

class Sprite(object):

    def __init__(self, id):
        self.id = id

    @classmethod
    def change_player(self, player):
        if player == Config.HUMAN:
            return Config.AI
        elif player == Config.AI:
            return Config.HUMAN
