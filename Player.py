from Sprite import Sprite

class Player(Sprite):

    def __init__(self, id):
        Sprite.__init__(self, id)
        self.last_position = None