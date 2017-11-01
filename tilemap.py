import pygame as pg
import math
from settings import *
vec = pg.math.Vector2

class Map:
    def __init__(self, filename):
        self.data = []
        self.saved_data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(list(line.strip()))

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    def update(self, row, col, mod = "."):
        if mod != ".":
            self.saved_data.remove((mod, row, col))
            self.data[row].pop(col)
        else:
            self.saved_data.append((self.data[row].pop(col), row, col))
        self.data[row].insert(col, mod)

    def find_player(self):
        for row, tiles in enumerate(self.data):
            for col, tile in enumerate(tiles):
                if tile == PLAYER_LETTER:
                    return col, row

class Camera:
    def __init__(self, width, height):
        self.pos = vec(0, 0)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.pos)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.pos.x = x
        self.pos.y = y

    def onscreen(self, entity):
        if -self.pos.x < entity.rect.x < (-self.pos.x + WIDTH) and -self.pos.y < entity.rect.y < (-self.pos.y + HEIGHT):
            return True
        return False

    def inside(self):
        row = math.floor(-self.pos.y / TILESIZE)
        col = math.floor(-self.pos.x / TILESIZE)
        return row, col
