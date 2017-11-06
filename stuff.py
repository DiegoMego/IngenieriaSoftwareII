import pygame as pg
from settings import *

class Obj:
    def __init__(self, x, y, width, height):
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

class Fence:
    def __init__(self, x, y, width, height):
        self.image_manager = ImageManager.get_instance()
        self.x = x
        self.y = y
        self.width = 160
        self.height = 320
        self.angle = 30

    def load_image(self, i_start, i_end):
        image = pg.Surface((160 ))
        for i in range(i_start, i_end + 1):
