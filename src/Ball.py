from random import random
from BresenhamsLineAlgorithm import bresenham


class Ball:
    x = 0
    y = 0
    direction = 0       # in degrees, 0° is up, 90° is right, 180° is down, 270° is left
    path = []           # path calculated with bresenham line algorithm
    bresenham = []

    def __init__(self,bresenham):
        self.set_ball()
        self.bresenham = bresenham

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
        self.y = random.randint(31, 32)


    def hit_ball(self):
        #hit results in returning the ball by random angle
        rnd = random.randint(-40,40)
        add_angle = 180 + rnd
        this.direction = this.direction + add_angle

    def calculate_path(self):
        #simulates the movement of the ball
        units = 10
        old_x = self.x
        old_y = self.y
        x = self.x + sin(direction) * units
        y = self.y + cos(direction) * untis
        pixel_start = Pixel(old_x,old_y)
        pixel_end = Pixel(x, y)

        self.path = self.bresenham(pixel_start, pixel_end)

    def move_ball(self):
        for i in range(len(self.path)):
            self.update_position()
           #delete first element of path
            self.path.pop()
            #display curr position TODO

