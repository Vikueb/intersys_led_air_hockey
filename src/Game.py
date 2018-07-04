from Matrix import Matrix
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as Bla


class Game:
    bresenham = None
    matrix = None

    def __init__(self):
        self.matrix = Matrix()
        self.bresenham = Bla(self.matrix)
        self.setup_gpio()
        self.setup_camera()
        self.loop()

    def setup_gpio(self):
        # pin setup
        pass

    def setup_camera(self):
        # camera setup
        pass

    def loop(self):
        # game loop
        pass
