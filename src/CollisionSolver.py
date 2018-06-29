from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm
from Matrix import Matrix


class SolveCollision:
    previouspathtillcollision = []
    startX = 0
    startY = 0
    collisionX = 0
    collisionY = 0
    matrix = []

    def __init__(self, matrix, previouspathtillcollision, start, collisionpoint):
        self.startX = start.x
        self.startY = start.y
        self.collisionX = collisionpoint.x
        self.collisionY = collisionpoint.y
        self.previouspathtillcollision = previouspathtillcollision
        self.matrix = matrix

    def collisionsolver(self):
        # delta x&y
        dx = self.collisionX - self.startX
        dy = self.collisionY - self.startY

        # mirrorpoint for help

        mirrorX = self.collisionX + dx
        mirrorY = self.collisionY + dy

        # Ponit on axis below mirrorpoint to generate new (true) mirrorpoint, which we need
        axisX = 0
        axisY = 0

        if self.collisionX == 0:
            axisX = 0
            axisY = mirrorY

        if self.collisionX == 63:
            axisX = 63
            axisY = mirrorY

        if self.collisionY == 0:
            axisY = 0
            axisX = mirrorX

        if self.collisionY == 31:
            axisY = 31
            axisX = mirrorX

        # mirrorpoint that we need

        dxnew = axisX - mirrorX
        dynew = axisY - mirrorY

        truemirrorX = axisX + dxnew
        truemirrorY = axisY + dynew

        # append new path from collisionpoint till truemirrorpoint to previouspath
        pixelcollision = Matrix.Pixel(self.collisionX, self.collisionY)
        truemirrorpixel = Matrix.Pixel(truemirrorX, truemirrorY)
        bresen = BresenhamsLineAlgorithm(self.matrix)
        newpath = bresen.calculate(pixelcollision, truemirrorpixel)

        # drop first element, which is the wall
        newpath.pop(0)

        # now append both paths and return them
        a = self.previouspathtillcollision.append(newpath)

        return a