import pygame as pg
from settings import *

class Stuff(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def load_image(self, spritesheet, x, y):
        self.image = pg.Surface((self.width, self.height))
        self.image.blit(spritesheet, (0, 0), (x, y, self.width, self.height))
        self.image.set_colorkey(FUCHSIA)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
