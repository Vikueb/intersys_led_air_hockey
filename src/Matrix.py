from Ball import Ball
import numpy as np
# import RPi.GPIO as gpio


class Matrix:
    # nodes define a 32 times 64 array array where x_Max is 32 and y_Max is 64
    x_Max = 64
    y_Max = 32
    board = []
    ball = None
    goal_player1 = (0, np.arange(12, 20, 1))
    goal_player2 = (63, np.arange(12, 20, 1))

    def __init__(self):
        self.board = self.field()
        self.ball = Ball()

        return

    def field(self):
        field = []
        for y in range(self.y_Max):
            new_line = []
            for x in range(self.x_Max):
                new_line.append(Pixel(x, y))

            field.append(new_line)

        return field

    def draw(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        pass

    def is_goal(self, x, y):
        if x == 0:
            if y == (g for g in self.goal_player1[1]):
                return 1
        else:
            if x == 63:
                if y == (g for g in self.goal_player1[1]):
                    return 0

        return -1


class Pixel:
    x = 0
    y = 0

    def __init__(self, x_value, y_value):
        self.x = x_value
        self.y = y_value
