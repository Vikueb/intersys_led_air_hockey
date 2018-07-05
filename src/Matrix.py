from Ball import Ball
import numpy as np
import RPi.GPIO as GPIO


class Matrix:
    # nodes define a 32 times 64 array array where x_Max is 32 and y_Max is 64
    x_Max = 63
    y_Max = 31
    board = []
    ball = None
    goal_player1 = (0, np.arange(12, 20, 1))
    goal_player2 = (63, np.arange(12, 20, 1))

    def __init__(self):
        self.board = self.field()

        return

    def field(self):
        field = []
        for y in range(self.y_Max):
            new_line = []
            for x in range(self.x_Max):
                new_line.append(Pixel(x, y))

            field.append(new_line)

        return field

    def draw_pixel(self, x, y):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix

        return

    def draw_line_vertical(self, x, y_down, y_up):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(y_down, y_up+1, 1)
        for y in line:
            self.draw_pixel(x, y)

        return

    def draw_line_horizontal(self, x_left, x_right, y):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(x_left, x_right+1, 1)
        for x in line:
            self.draw_pixel(x, y)

        return

    def draw_goals(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        self.draw_line_vertical(0,  self.goal_player1[1][0], self.goal_player1[1][len(self.goal_player1[1]-1)])
        self.draw_line_vertical(63, self.goal_player2[1][0], self.goal_player2[1][len(self.goal_player2[1]-1)])
        return

    def draw_standby(self):
        self.draw_line_vertical(0, 0, 31)
        self.draw_line_vertical(63, 0, 31)
        self.draw_line_horizontal(0, 63, 0)
        self.draw_line_horizontal(0, 63, 31)
        return

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
