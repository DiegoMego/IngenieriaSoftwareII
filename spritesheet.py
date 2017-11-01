import pygame as pg
from os import path
from settings import *

class SpriteSheet:
    def get_image(self, x, y, width, height, img_x = 16, img_y = 16):
        image = pg.Surface((128, 128))
        image.fill(WHITE)
        image.blit(self.image, (img_x, img_y), (x, y, width, height))
        image.set_colorkey(WHITE)
        return image

    def get_terrain(self, x, y):
        image = pg.Surface((160, 80))
        image.fill(WHITE)
        image.blit(self.image, (0, 0), (x, y, 160, 80))
        image.set_colorkey(FUCHSIA)
        return image
