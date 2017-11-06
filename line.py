import pygame as pg
vec = pg.math.Vector2

class Line:
    def __init__(self, x_start, x_end):
        self.x_start = x_start
        self.x_end = x_end

    def check(self, pos):
        points = []
        for x in range(self.x_start, self.x_end + 1):
            y = -2 * x
            points.append(vec(x - pos.x, y - pos.y))
        return points
