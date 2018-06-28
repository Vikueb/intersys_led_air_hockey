from Matrix import Matrix
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as bla


class Game:
    def __init__(self):
        self.matrix = Matrix()
        self.bresenham = bla(self.matrix)

