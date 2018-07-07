from random import random
import math


class Ball:
    x = 0
    y = 0
    direction = 0       # in degrees, 0 is right, 90 is up, 180 is left, 270 is down
    path = []           # path calculated with bresenham line algorithm

# ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self, bresenham):
        random.seed()
        self.set_ball(-1)
        self.bresenham = bresenham

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
            self.direction = random.randint(320, 400) % 360     # right
        else:
            self.x = 42
            self.direction = random.randint(140, 220)           # left
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
        # update path
        units = 10
        x = self.x + int(math.sin(math.radians(self.direction))) * units
        y = self.y + int(math.cos(math.radians(self.direction))) * units

        self.path = self.bresenham.calculate(self.x, self.y, x, y)

        # update degrees
        dx = self.x - x
        dy = self.y - y
        h = math.sqrt(dx**2 + dy**2)

        if dx < 0 & dy < 0:
            self.direction = 270 + math.degrees(math.acos(math.fabs(dx) / h))
        else:
            if dx < 0 & dy >= 0:
                self.direction = 0 + math.degrees(math.acos(dy / h))
            else:
                if dx >= 0 & dy < 0:
                    self.direction = 180 + math.degrees(math.acos(math.fabs(dy) / h))
                else:
                    # if dx >= 0 &  dy >= 0:
                    self.direction = 90 + math.degrees(math.acos(math.fabs(dx) / h))

        return

# ---------------------------------------------------------------------------------------------------------------- #
    def move(self):
        self.update_position()

        if len(self.path) < 5:
            self.calculate_path()

        return



