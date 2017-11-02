import pygame as pg
from os import *
from settings import *
from imagemanager import *
from spritesheet import *

# class HUD:
#     def __init__(self):
#         self.image_manager = ImageManager.get_instance()
#         self.spritesheet = SpriteSheet.get_instance()
#
#     def load(self):
#         pass
#
#     def get(self):
#         pass

class HUD(pg.sprite.Sprite):
    _LIFE_PATH = "Life.png"

    @classmethod
    def get_full_life_path(cls):
        return cls._LIFE_PATH

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.spritesheet = SpriteSheet.get_instance()
        self.spritesheet.add_sprite(self, HUD_FOLDER, self.get_full_life_path())
        self.image = self.load_life()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((0, HEIGHT))

    def load_life(self):
        self.width = 160
        self.height = 128
        self.backlife = self.image_manager.get_image(self.spritesheet.get_sprite(self), 0, 0, self.width, self.height)
        self.frontlife = self.image_manager.get_image(self.spritesheet.get_sprite(self), 0, self.height, self.width, self.height)
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
