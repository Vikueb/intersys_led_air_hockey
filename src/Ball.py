from random import random


class Ball:
    x = 0
    y = 0
    direction = 0       # in degrees, 0° is up, 90° is right, 180° is down, 270° is left
    path = []           # path calculated with bresenham line algorithm

    def __init__(self):
        self.set_ball()

    def update_position(self):
        point = self.path[0]
        self.x = point.x
        self.y = point.y

    def set_ball(self):
        start = random.randint(0, 1)
        if start == 0:
            self.x = 21
            self.direction = random.randint(50, 130)
        else:
            self.x = 42
            self.direction = random.randint(230, 310)
        self.x = random.randint(31, 32)
