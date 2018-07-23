import numpy as np


class Player:

    def __init__(self, identity):
        self.id = identity
        self.score = 0
        self.x = np.zeros([4])
        self.y = np.zeros([4])

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def set_position(self, new_x, new_y):
        """
        sets the position of the player according to the hand middle detected
        :param new_x: x position detected
        :param new_y: y position detected
        :return: reserves 4 positions for the player, void
        """
        self.x = np.zeros([4])
        self.y = np.zeros([4])
        self.x[0] = new_x
        self.x[1] = new_x
        if new_x < 63:
            self.x[2] = new_x+1
            self.x[3] = new_x+1
        else:
            self.x[2] = new_x-1
            self.x[3] = new_x-1

        self.y[0] = new_y
        self.y[2] = new_y
        if new_y < 31:
            self.y[1] = new_y+1
            self.y[3] = new_y+1
        else:
            self.y[1] = new_y-1
            self.y[3] = new_y-1

        return
