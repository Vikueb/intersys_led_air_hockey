class BresenhamsLineAlgorithm:

    def __init__(self, matrix):
        self.matrix = matrix
        self.max_x = len(matrix)
        self.max_y = len(matrix[0])

    def calculate(self, start_pixel, end_pixel):
        path = []
        start_x = start_pixel.x
        start_y = start_pixel.y
        end_x = end_pixel.x
        end_y = end_pixel.y
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
                        return path
                    path.append(self.matrix[start_x][start_y - p])
            else:
                if dy < 0:
                    # startpoint is lower as endpoint
                    for p in range(abs(start_y - end_y)):
                        if self.out_of_range(start_x, start_y + p):
                            return path
                        path.append(self.matrix[start_x][start_y + p])
            return path

        if dy == 0:
            if dx > 0:
                # startpoint is further right than endpoint
                for p in range(start_x - end_x):
                    if self.out_of_range(start_x - p, start_y):
                        return path
                    path.append(self.matrix[start_x - p][start_y])
            else:
                if dx < 0:
                    # startpoint is further left than endpoint
                    for p in range(abs(start_x - end_x)):
                        if self.out_of_range(start_x + p, start_y):
                            return path
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
                            return path
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
                                return path
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
                            return path
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
                                return path
                            path.append(self.matrix[x][start_y - p])
                            err += derr
                            if err >= half:
                                if dx > 0:
                                    x += 1
                                else:
                                    x -= 1
                                err -= 1
            return path

    def out_of_range(self, x, y):
        return x < 0 | y < 0 | x > self.max_x | y > self.max_y
