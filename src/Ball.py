from random import random
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as Bla
from Matrix import Pixel
import math


class Ball:
    x = 0
    y = 0
    direction = 0       # in degrees, 0° is up, 90° is right, 180° is down, 270° is left
    path = []           # path calculated with bresenham line algorithm
    bresenham = []

# ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self, matrix):
        self.set_ball(-1)
        self.bresenham = Bla(matrix)

# ---------------------------------------------------------------------------------------------------------------- #
    def update_position(self):
        point = self.path[0]
        self.x = point.x
        self.y = point.y

        for i in range(len(self.path) - 1):
            if i != 0:
                self.path[i-1] = self.path[i]

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def set_ball(self, rand):
        if rand == -1:
            start = random.randint(0, 1)
        else:
            start = rand
        if start == 0:
            self.x = 21
            self.direction = random.randint(50, 130)
        else:
            self.x = 42
            self.direction = random.randint(230, 310)
        self.y = random.randint(31, 32)

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def hit_ball(self):
        # hit results in returning the ball by random angle
        rnd = random.randint(-40, 40)
        add_angle = 180 + rnd
        self.direction = (self.direction + add_angle) % 360

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def calculate_path(self):
        # simulates the future movement of the ball
        units = 10
        x = self.x + int(math.sin(self.direction) * units)
        y = self.y + int(math.cos(self.direction) * units)
        pixel_start = Pixel(self.x, self.y)
        pixel_end = Pixel(x, y)

        self.path = self.bresenham.calculate(pixel_start, pixel_end)

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def move(self):
        self.update_position()

        if len(self.path) < 5:
            self.calculate_path()

        return



