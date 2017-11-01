import pygame as pg
from os import *
from settings import *
from imagemanager import *

class HUD(pg.sprite.Sprite):
    __EMPTY_LIFE_PATH = path.join(HUD_FOLDER, "Empty Life Orb.png")
    __FULL_LIFE_PATH = path.join(HUD_FOLDER, "Life Orb.png")

    @classmethod
    def get_full_life_path(cls):
        return cls.__FULL_LIFE_PATH

    @classmethod
    def get_empty_life_path(cls):
        return cls.__EMPTY_LIFE_PATH

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.image = self.load_life()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((0, HEIGHT))

    def load_life(self):
        self.width = 160
        self.height = 128
        self.backlife = self.image_manager.get_image(self.get_empty_life_path(), 0, 0, self.width, self.height)
        self.frontlife = self.image_manager.get_image(self.get_full_life_path(), 0, 0, self.width, self.height)
        self.frontlife.set_colorkey((0, 1, 0))
        image = pg.Surface((self.width, self.height))
        image.blit(self.backlife, (0, 0))
        image.blit(self.frontlife, (0, 0))
        image.set_colorkey((BLACK))
        return image

    def get_life(self, n):
        self.image.fill((WHITE))
        self.image.blit(self.backlife, (0, 0))
        self.image.blit(self.frontlife, (0, self.height * n), (0, self.height * n, self.width, self.height))
