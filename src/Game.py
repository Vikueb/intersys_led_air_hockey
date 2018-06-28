import sys
# sys.path.append("C:\\Users\\vkueb\\PycharmProjects\\intersys_led_air_hockey\\src")
import Matrix
import BresenhamsLineAlgorithm


class Game:
    def __init__(self):
        self.matrix = Matrix()
        self.bresenham = BresenhamsLineAlgorithm(self.matrix)

