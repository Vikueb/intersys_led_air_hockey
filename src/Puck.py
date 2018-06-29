class Puck:
    positionX = 0
    positionY = 0
    direction = 0

    def __init__(self, position, direction):
        self.positionX = position.x
        self.positionY = position.y
        self.direction = direction

    def update_direction(self, direction):
        self.direction = direction

    def update_position(self, new_position):
        self.positionX = new_position.x
        self.positionY = new_position.y