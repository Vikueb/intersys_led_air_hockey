import numpy as np
import random
import RPi.GPIO as GPIO


class Matrix:

    def __init__(self):
        """
        the matrix is a 32 times 64 array where x_Max is 31 and y_Max is 63 (because indexes start with 0)
        """
        self.x_Max = 63
        self.y_Max = 31
        self.goal_player1 = (0, np.arange(12, 20, 1))
        self.goal_player2 = (63, np.arange(12, 20, 1))
        self.field = self.field()

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def field(self):
        """
        # watch out! looks like this:
        # ---x-------------------------------------------------------- #
        # y (0,0) (1,0) (2,0) (3,0) (4,0) ...
        # | (0,1) (1,1) (2,1) (3,1) ...
        # | (0,2) (1,2) (2,2)  ...
        # | (0,3) (1,3) ...
        # | (0,4) ...
        # | ...
        # ------------------------------------------------------------ #
        :return: the empty array
        """

        field = np.chararray((self.y_Max, self.x_Max))

        return field

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_pixel(self, x, y, string):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        self.field[y][x] = string

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_line_vertical(self, x, y_up, y_down):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(y_up, y_down + 1, 1)
        for y in line:
            self.draw_pixel(x, y, "|")

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_line_horizontal(self, x_left, x_right, y):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(x_left, x_right+1, 1)
        for x in line:
            self.draw_pixel(x, y, "-")

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_goals(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # color red
        self.draw_line_vertical(0,  self.goal_player1[1][0], self.goal_player1[1][len(self.goal_player1[1]-1)])
        self.draw_line_vertical(63, self.goal_player2[1][0], self.goal_player2[1][len(self.goal_player2[1]-1)])
        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_standby(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # changing color
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.draw_line_vertical(0, 0, 31)
        self.draw_line_vertical(63, 0, 31)
        self.draw_line_horizontal(0, 63, 0)
        self.draw_line_horizontal(0, 63, 31)
        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_circle(self, x_middle, y_middle):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # r = 5, color = green
        # upper half
        self.draw_pixel(x_middle + 5, y_middle, "|")
        self.draw_pixel(x_middle + 5, y_middle + 1, "\\")
        self.draw_pixel(x_middle + 4, y_middle + 2, "|")
        self.draw_pixel(x_middle + 4, y_middle + 3, "\\")
        self.draw_pixel(x_middle + 3, y_middle + 4, "-")
        self.draw_pixel(x_middle + 2, y_middle + 4, "\\")
        self.draw_pixel(x_middle + 1, y_middle + 5, "-")
        self.draw_pixel(x_middle + 0, y_middle + 5, "-")
        self.draw_pixel(x_middle - 1, y_middle + 5, "-")
        self.draw_pixel(x_middle - 2, y_middle + 4, "/")
        self.draw_pixel(x_middle - 3, y_middle + 4, "-")
        self.draw_pixel(x_middle - 4, y_middle + 3, "/")
        self.draw_pixel(x_middle - 4, y_middle + 2, "|")
        self.draw_pixel(x_middle - 5, y_middle + 1, "/")
        # lower half
        self.draw_pixel(x_middle - 5, y_middle, "|")
        self.draw_pixel(x_middle - 5, y_middle - 1, "\\")
        self.draw_pixel(x_middle - 4, y_middle - 2, "|")
        self.draw_pixel(x_middle - 4, y_middle - 3, "\\")
        self.draw_pixel(x_middle - 3, y_middle - 4, "-")
        self.draw_pixel(x_middle - 2, y_middle - 4, "\\")
        self.draw_pixel(x_middle - 1, y_middle - 5, "-")
        self.draw_pixel(x_middle - 0, y_middle - 5, "-")
        self.draw_pixel(x_middle + 1, y_middle - 5, "-")
        self.draw_pixel(x_middle + 2, y_middle - 4, "/")
        self.draw_pixel(x_middle + 3, y_middle - 4, "-")
        self.draw_pixel(x_middle + 4, y_middle - 3, "/")
        self.draw_pixel(x_middle + 4, y_middle - 2, "|")
        self.draw_pixel(x_middle + 5, y_middle - 1, "/")

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def is_goal(self, x, y):
        """
        checks whether the ball equals a point in a goal
        :param x: the x value of the ball
        :param y: the y value of the ball
        :return: the id of the player who hit the goal, or -1 when none was hit
        """
        if x == 0:
            left = False
            for g in self.goal_player1[1]:
                left |= y == g
            if left:
                return 1
        if x == 63:
            right = False
            for g in self.goal_player1[1]:
                right |= y == g
            if right:
                return 0

        return -1

# ---------------------------------------------------------------------------------------------------------------- #
