class Player:

    def __init__(self, identity):
        self.id = identity
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y
