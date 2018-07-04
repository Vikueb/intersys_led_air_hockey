from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm
from Matrix import Matrix


class SolveCollision:
    previous_path_till_collision = []
    startX = 0
    startY = 0
    collisionX = 0
    collisionY = 0
    matrix = []

    def __init__(self, matrix, previous_path_till_collision, start, collision_point):
        self.startX = start.x
        self.startY = start.y
        self.collisionX = collision_point.x
        self.collisionY = collision_point.y
        self.previous_path_till_collision = previous_path_till_collision
        self.matrix = matrix

    def collision_solver(self):
        # delta x&y
        dx = self.collisionX - self.startX
        dy = self.collisionY - self.startY

        # mirror_point for help

        mirror_x = self.collisionX + dx
        mirror_y = self.collisionY + dy

        # Point on axis below mirror_point to generate new (true) mirror_point, which we need
        axis_x = 0
        axis_y = 0

        if self.collisionX == 0:
            axis_x = 0
            axis_y = mirror_y

        if self.collisionX == 63:
            axis_x = 63
            axis_y = mirror_y

        if self.collisionY == 0:
            axis_y = 0
            axis_x = mirror_x

        if self.collisionY == 31:
            axis_y = 31
            axis_x = mirror_x

        if self.collisionX == 0 and self.collisionY == 0:
            axis_x = 0
            axis_y = 0

        if self.collisionX == 63 and self.collisionY == 0:
            axis_x = 63
            axis_y = 0

        if self.collisionX == 0 and self.collisionY == 31:
            axis_x = 0
            axis_y = 31

        if self.collisionX == 63 and self.collisionY == 31:
            axis_x = 63
            axis_y = 31
        # mirror_point that we need

        dx_new = axis_x - mirror_x
        dy_new = axis_y - mirror_y

        true_mirror_x = axis_x + dx_new
        true_mirror_y = axis_y + dy_new

        # append new path from collision_point till true_mirror_point to previous_path_till_collision
        pixel_collision = Matrix.Pixel(self.collisionX, self.collisionY)
        true_mirror_pixel = Matrix.Pixel(true_mirror_x, true_mirror_y)
        bresenham = BresenhamsLineAlgorithm(self.matrix)
        new_path = bresenham.calculate(pixel_collision, true_mirror_pixel)

        # drop first element, which is the wall
        new_path.pop(0)

        # now append both paths and return them
        a = self.previous_path_till_collision.append(new_path)

        return a
