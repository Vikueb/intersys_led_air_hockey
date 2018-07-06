from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm
from Matrix import Pixel
import math


class SolveCollision:

    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.collision_x = 0
        self.collision_y = 0
        self.matrix = None
        self.bresenham = BresenhamsLineAlgorithm(self.matrix)

# ---------------------------------------------------------------------------------------------------------------- #
    def collision_solver(self, matrix, start, path, collision_point, x_or_y):
        self.start_x = start.x
        self.start_y = start.y
        self.collision_x = collision_point.x
        self.collision_y = collision_point.y
        self.matrix = matrix

        if x_or_y == "x":
            mirror_x, mirror_y = self.collision_on_x_axis()
        else:
            # y is the collision axis
            mirror_x, mirror_y = self.collision_on_y_axis()

        # calculate new path from collision_point to mirror_point
        new_path = self.bresenham.calculate(self.collision_x, self.collision_y, mirror_x, mirror_y)

        # drop first element, which is the wall
        new_path.pop(0)

        # now append both paths and return them
        path = path + new_path

        return path

# ---------------------------------------------------------------------------------------------------------------- #
    def collision_on_y_axis(self):
        # delta y
        dy = self.collision_y - self.start_y

        mirror_x = self.start_x
        mirror_y = 0

        if dy < 0:
            mirror_y = self.start_y + 2 * math.fabs(dy)
        else:
            if dy >= 0:
                mirror_y = self.start_y - 2 * math.fabs(dy)

        return mirror_x, mirror_y

# ---------------------------------------------------------------------------------------------------------------- #
    def collision_on_x_axis(self):
        # delta x
        dx = self.collision_x - self.start_x

        mirror_x = 0
        mirror_y = self.start_y

        if dx < 0:
            mirror_x = self.start_x + 2 * math.fabs(dx)
        else:
            if dx >= 0:
                mirror_x = self.start_x - 2 * math.fabs(dx)

        return mirror_x, mirror_y
