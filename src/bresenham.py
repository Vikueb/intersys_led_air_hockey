class bresenhamsLineAlgorithm:
    matrix = []
    path = []
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    dx = 0
    dy = 0

    def __init__ (self, matrix, start_pixel, end_pixel):
        self.startX = start_pixel.x
        self.startY = start_pixel.y
        self.endX = end_pixel.x
        self.endY = end_pixel.y
        self.matrix = matrix
        self.dx = self.startX - self.endX
        self.dy = self.startY - self.endY

    def calculate(self):
        half = 0.5

        if self.dx == 0 & self.dy == 0:
            self.path.append(self.matrix[self.startX][self.startY])
            return self.path

        if self.dx == 0:
            if self.dy > 0:
                # startpoint is higher as endpoint
                for p in range(self.startY - self.endY):
                    self.path.append(self.matrix[self.startX][self.startY - p])
            else:
                if self.dy < 0:
                    # startpoint is lower as endpoint
                    for p in range(abs(self.startY - self.endY)):
                        self.path.append(self.matrix[self.startX][self.startY + p])
            return self.path

        if self.dy == 0:
            if self.dx > 0:
                # startpoint is further right than endpoint
                for p in range(self.startX - self.endX):
                    self.path.append(self.matrix[self.startX - p][self.startY])
            else:
                if self.dx < 0:
                    # startpoint is further left than endpoint
                    for p in range(abs(self.startX - self.endX)):
                        self.path.append(self.matrix[self.startX + p][self.startY])
            return self.path

        if self.dx != 0 & self.dy != 0:
            derr = abs(self.dy) / abs(self.dx)
            err = derr - half
            if abs(self.dx) >= abs(self.dy):
                y = self.startY
                # startpoint further left than endpoint
                if self.dx < 0:
                    for p in range(abs(self.startX - self.endX)):
                        self.path.append(self.matrix[self.startX + p][y])
                        err += derr
                        if err >= half:
                            if self.dy > 0:
                                y += 1
                            else :
                                y -= 1
                            err -= 1
                else:
                    # startpoint further right than endpoint
                    if self.dx > 0:
                        for p in range(self.startX - self.endX):
                            self.path.append(self.matrix[self.startX - p][y])
                            err += derr
                            if err >= half:
                                if self.dy > 0:
                                    y += 1
                                else:
                                    y -= 1
            else:
                derr = abs(self.dx / self.dy)
                err = derr - half
                x = self.startX
                # startpoint lower than endpoint
                if self.dy < 0:
                    for p in range(abs(self.startY - self.endY)):
                        self.path.append(self.matrix[x][self.startX + p])
                        err += derr
                        if err >= half:
                            if self.dx > 0:
                                x += 1
                            else :
                                x -= 1
                            err -= 1
                else:
                    # startpoint higher than endpoint
                    if self.dy > 0:
                        for p in range(self.startY - self.endY):
                            self.path.append(self.matrix[x][self.startX - p])
                            err += derr
                            if err >= half:
                                if self.dx > 0:
                                    x += 1
                                else:
                                    x -= 1
                                err -= 1
            return self.path
