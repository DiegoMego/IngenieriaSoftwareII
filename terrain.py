import pygame as pg
import os
from settings import *
from spritesheet import *
vec = pg.math.Vector2

class Terrain(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = SpriteSheet("Maps\\" + "Act_1", "Town\\0.png")
        self.load_data()

    def load_data(self):
        self.image = pg.Surface((2560, 2560))
        self.terrain_image = pg.Surface((320, 160))
        self.images = []
        self.images.append(self.spritesheet.get_terrain(320, 80))
        self.images.append(self.spritesheet.get_terrain(0, 80))
        self.images.append(self.spritesheet.get_terrain(160, 80))
        self.images.append(self.spritesheet.get_terrain(640, 0))
        self.terrain_image.blit(self.images[0], (80, 0))
        self.terrain_image.blit(self.images[1], (0, 40))
        self.terrain_image.blit(self.images[2], (160, 40))
        self.terrain_image.blit(self.images[3], (80, 80))
        self.terrain_image.set_colorkey(BLACK)
        for y in range(-80, 2560, 160):
            for x in range(-160, 2560, 320):
                self.image.blit(self.terrain_image, (x, y))
                self.image.blit(self.terrain_image, (x + 160, y + 80))
        self.rect = self.image.get_rect()
