import math


class BresenhamsLineAlgorithm:

    def __init__(self, matrix):
        self.matrix = matrix
        self.max_x = len(matrix)
        self.max_y = len(matrix[0])

    def calculate(self, start_x, start_y, end_x, end_y):
        path = []
        dx = start_x - end_x
        dy = start_y - end_y

        half = 0.5

        if dx == 0 & dy == 0:
            path.append(self.matrix[start_x][start_y])
            return path

        if dx == 0:
            if dy > 0:
                # startpoint is higher as endpoint
                for p in range(start_y - end_y):
                    if self.out_of_range(start_x, start_y - p):
                        return self.solve_collision(start_x, start_y, path, start_x, start_y - p, 'x')
                    path.append(self.matrix[start_x][start_y - p])
            else:
                if dy < 0:
                    # startpoint is lower as endpoint
                    for p in range(abs(start_y - end_y)):
                        if self.out_of_range(start_x, start_y + p):
                            return self.solve_collision(start_x, start_y, path, start_x, start_y + p, 'x')
                        path.append(self.matrix[start_x][start_y + p])
            return path

        if dy == 0:
            if dx > 0:
                # startpoint is further right than endpoint
                for p in range(start_x - end_x):
                    if self.out_of_range(start_x - p, start_y):
                        return self.solve_collision(start_x, start_y, path, start_x - p, start_y, 'y')
                    path.append(self.matrix[start_x - p][start_y])
            else:
                if dx < 0:
                    # startpoint is further left than endpoint
                    for p in range(abs(start_x - end_x)):
                        if self.out_of_range(start_x + p, start_y):
                            return self.solve_collision(start_x, start_y, path, start_x + p, start_y, 'y')
                        path.append(self.matrix[start_x + p][start_y])
            return path

        if dx != 0 & dy != 0:
            derr = abs(dy) / abs(dx)
            err = derr - half
            if abs(dx) >= abs(dy):
                y = start_y
                # startpoint further left than endpoint
                if dx < 0:
                    for p in range(abs(start_x - end_x)):
                        if self.out_of_range(start_x + p, y):
                            return self.solve_collision(start_x, start_y, path, start_x + p, y, 'y')
                        path.append(self.matrix[start_x + p][y])
                        err += derr
                        if err >= half:
                            if dy > 0:
                                y += 1
                            else:
                                y -= 1
                            err -= 1
                else:
                    # startpoint further right than endpoint
                    if dx > 0:
                        for p in range(start_x - end_x):
                            if self.out_of_range(start_x - p, y):
                                return self.solve_collision(start_x, start_y, path, start_x - p, y, 'y')
                            path.append(self.matrix[start_x - p][y])
                            err += derr
                            if err >= half:
                                if dy > 0:
                                    y += 1
                                else:
                                    y -= 1
            else:
                derr = abs(dx / dy)
                err = derr - half
                x = start_x
                # startpoint lower than endpoint
                if dy < 0:
                    for p in range(abs(start_y - end_y)):
                        if self.out_of_range(x, start_y + p):
                            return self.solve_collision(start_x, start_y, path, x, start_y + p, 'x')
                        path.append(self.matrix[x][start_y + p])
                        err += derr
                        if err >= half:
                            if dx > 0:
                                x += 1
                                x -= 1
                            err -= 1
                else:
                    # startpoint higher than endpoint
                    if dy > 0:
                        for p in range(start_y - end_y):
                            if self.out_of_range(x, start_y - p):
                                return self.solve_collision(start_x, start_y, path, x, start_y - p, 'x')
                            path.append(self.matrix[x][start_y - p])
                            err += derr
                            if err >= half:
                                if dx > 0:
                                    x += 1
                                else:
                                    x -= 1
                                err -= 1
        return path

# ---------------------------------------------------------------------------------------------------------------- #
    def out_of_range(self, x, y):
        return x < 0 | y < 0 | x > self.max_x | y > self.max_y

# ---------------------------------------------------------------------------------------------------------------- #
    def solve_collision(self, start_x, start_y, path, collision_x, collision_y, x_or_y):

        # to not diverge, keeping looks in the future short
        if len(path) > 10:
            return

        if not self.corner(collision_x, collision_y):
            if x_or_y == 'x':
                mirror_x, mirror_y = self.collision_on_x_axis(start_x, start_y, collision_y)
            else:
                # y is the collision axis
                mirror_x, mirror_y = self.collision_on_y_axis(start_x, start_y, collision_x)
        else:
            mirror_x = start_x
            mirror_y = start_y

        # calculate new path from collision_point to mirror_point
        new_path = self.calculate(collision_x, collision_y, mirror_x, mirror_y)

        # drop first element, which is the wall
        new_path.pop(0)

        # now append both paths and return them
        path = path + new_path

        return path

# ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def corner(collision_x, collision_y):
        left_upper = collision_x == 0 | collision_y == 0
        left_lower = collision_x == 0 | collision_y == 31
        right_upper = collision_x == 63 | collision_y == 0
        right_lower = collision_x == 63 | collision_y == 31

        return left_upper | left_lower | right_upper | right_lower

# ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def collision_on_y_axis(start_x, start_y, collision_y):
        # delta y
        dy = collision_y - start_y

        mirror_x = start_x
        mirror_y = 0

        if dy < 0:
            mirror_y = start_y + 2 * math.fabs(dy)
        else:
            if dy >= 0:
                mirror_y = start_y - 2 * math.fabs(dy)

        return mirror_x, mirror_y

# ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def collision_on_x_axis(start_x, start_y, collision_x):
        # delta x
        dx = collision_x - start_x

        mirror_x = 0
        mirror_y = start_y

        if dx < 0:
            mirror_x = start_x + 2 * math.fabs(dx)
        else:
            if dx >= 0:
                mirror_x = start_x - 2 * math.fabs(dx)

        return mirror_x, mirror_y
