from random import random


class Ball:
    x = 0
    y = 0
    direction = 0       # in degrees, 0° is up, 90° is right, 180° is down, 270° is left
    path = []           # path calculated ba bresenham line algorithm

    def __init__(self):
        x_start = random.randint(16, 17)
        y_start = random.randint(32, 33)

        self.x = x_start
        self.y = y_start

    def update_position(self, point):
        self.x = point.x
        self.y = point.y
