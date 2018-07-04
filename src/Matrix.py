import random as random
# import RPi.GPIO as gpio


class Matrix:
    # nodes define a 32 times 64 array array where x_Max is 32 and y_Max is 64
    x_Max = 64
    y_Max = 32
    board = []
    start = None
    goal_player1 = []
    goal_player2 = []

    def __init__(self):
        self.board = self.field()
        x_start = random.randint(16, 17)
        y_start = random.randint(32, 33)
        self.start = self.Pixel(x_start, y_start)

        return

    def field(self):
        field = []
        for y in range(self.y_Max):
            new_line = []
            for x in range(self.x_Max):
                new_line.append(self.Pixel(x, y))

            field.append(new_line)

        return field

    class Pixel:
        x = 0
        y = 0

        def __init__(self, x_value, y_value):
            self.x = x_value
            self.y = y_value
