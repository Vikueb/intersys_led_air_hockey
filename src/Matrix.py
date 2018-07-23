import numpy as np
import random
import RPi.GPIO as GPIO


class Matrix:

    def __init__(self, pins):
        """
        the matrix is a 32 times 64 array where x_Max is 31 and y_Max is 63 (because indexes start with 0)
        """
        # pins : [LAT, clock, OE,  A,  B,  C,  D, R1, G1, B1, R2, G2, B2]
        self.pins = pins
        self.x_Max = 63
        self.y_Max = 31
        self.goal_player1 = (0, np.arange(12, 20, 1))
        self.goal_player2 = (63, np.arange(12, 20, 1))
        self.field = self.field()
        self.board = self.board()

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def board(self):

        board = []
        for i in range(self.x_Max+1):
            column = []
            for j in range(self.y_Max+1):
                column.append(self.Point(i, j))
            board.append(column)

        return board

# ---------------------------------------------------------------------------------------------------------------- #
    def field(self):

        field = np.chararray((self.x_Max+1, self.y_Max+1))

        return field

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_pixel(self, x, y, string, color):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # pins : [LAT, OE,  A,  B,  C,  D, R1, G1, B1, R2, G2, B2, clock]
        #        [  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11,    12]
        self.field[x][y] = string

        GPIO.output(self.pins[2], GPIO.HIGH)
        GPIO.output(self.pins[3], GPIO.HIGH)
        GPIO.output(self.pins[4], GPIO.HIGH)
        GPIO.output(self.pins[5], GPIO.HIGH)
        GPIO.output(self.pins[6], GPIO.HIGH)
        GPIO.output(self.pins[12], GPIO.HIGH)

        GPIO.output(self.pins[12], GPIO.LOW)
        GPIO.output(self.pins[6], GPIO.LOW)
        GPIO.output(self.pins[5], GPIO.LOW)
        GPIO.output(self.pins[4], GPIO.LOW)
        GPIO.output(self.pins[3], GPIO.LOW)
        GPIO.output(self.pins[2], GPIO.LOW)

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_line_vertical(self, x, y_up, y_down, color):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(y_up, y_down + 1, 1)
        for y in line:
            self.draw_pixel(x, y, "|", color)

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_line_horizontal(self, x_left, x_right, y, color):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        line = np.arange(x_left, x_right+1, 1)
        for x in line:
            self.draw_pixel(x, y, "-", color)

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_goals(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # color red
        self.draw_line_vertical(0,  self.goal_player1[1][0], self.goal_player1[1][len(self.goal_player1[1])-1], (255, 0, 0))
        self.draw_line_vertical(63, self.goal_player2[1][0], self.goal_player2[1][len(self.goal_player2[1])-1], (255, 0, 0))
        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_standby(self):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # changing color
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.draw_line_vertical(0, 0, 31, (red, green, blue))
        self.draw_line_vertical(63, 0, 31, (red, green, blue))
        self.draw_line_horizontal(0, 63, 0, (red, green, blue))
        self.draw_line_horizontal(0, 63, 31, (red, green, blue))
        return

# ---------------------------------------------------------------------------------------------------------------- #
    def draw_circle(self, x_middle, y_middle, color):
        # https://www.hackster.io/idreams/getting-started-with-rgb-matrix-panel-adaa49
        # https://github.com/hzeller/rpi-rgb-led-matrix
        # r = 5, color = green
        # upper half
        self.draw_pixel(x_middle + 5, y_middle, "|", color)
        self.draw_pixel(x_middle + 5, y_middle + 1, "\\", color)
        self.draw_pixel(x_middle + 4, y_middle + 2, "|", color)
        self.draw_pixel(x_middle + 4, y_middle + 3, "\\", color)
        self.draw_pixel(x_middle + 3, y_middle + 4, "-", color)
        self.draw_pixel(x_middle + 2, y_middle + 4, "\\", color)
        self.draw_pixel(x_middle + 1, y_middle + 5, "-", color)
        self.draw_pixel(x_middle + 0, y_middle + 5, "-", color)
        self.draw_pixel(x_middle - 1, y_middle + 5, "-", color)
        self.draw_pixel(x_middle - 2, y_middle + 4, "/", color)
        self.draw_pixel(x_middle - 3, y_middle + 4, "-", color)
        self.draw_pixel(x_middle - 4, y_middle + 3, "/", color)
        self.draw_pixel(x_middle - 4, y_middle + 2, "|", color)
        self.draw_pixel(x_middle - 5, y_middle + 1, "/", color)
        # lower half
        self.draw_pixel(x_middle - 5, y_middle, "|", color)
        self.draw_pixel(x_middle - 5, y_middle - 1, "\\", color)
        self.draw_pixel(x_middle - 4, y_middle - 2, "|", color)
        self.draw_pixel(x_middle - 4, y_middle - 3, "\\", color)
        self.draw_pixel(x_middle - 3, y_middle - 4, "-", color)
        self.draw_pixel(x_middle - 2, y_middle - 4, "\\", color)
        self.draw_pixel(x_middle - 1, y_middle - 5, "-", color)
        self.draw_pixel(x_middle - 0, y_middle - 5, "-", color)
        self.draw_pixel(x_middle + 1, y_middle - 5, "-", color)
        self.draw_pixel(x_middle + 2, y_middle - 4, "/", color)
        self.draw_pixel(x_middle + 3, y_middle - 4, "-", color)
        self.draw_pixel(x_middle + 4, y_middle - 3, "/", color)
        self.draw_pixel(x_middle + 4, y_middle - 2, "|", color)
        self.draw_pixel(x_middle + 5, y_middle - 1, "/", color)

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
    class Point:

        def __init__(self, x, y):
            self.x = x
            self.y = y
