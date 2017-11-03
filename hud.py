import pygame as pg
from os import *
from settings import *
from imagemanager import *

class Life(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.image = self.load_life()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((0, HEIGHT))

    def load_life(self):
        self.width = 160
        self.height = 128
        backlife, frontlife = self.image_manager.get_hud_images()
        self.backlife_sprite = backlife
        self.frontlife_sprite = frontlife
        self.frontlife_sprite.set_colorkey((0, 1, 0))
        image = pg.Surface((self.width, self.height))
        image.blit(self.backlife_sprite, (0, 0))
        image.blit(self.frontlife_sprite, (0, 0))
        image.set_colorkey((BLACK))
        return image

    def get_life(self, n):
        self.image.fill((WHITE))
        self.image.blit(self.backlife_sprite, (0, 0))
        self.image.blit(self.frontlife_sprite, (0, self.height * n), (0, self.height * n, self.width, self.height))

class Mana(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.image = self.load_life()
        self.rect = self.image.get_rect()
        self.rect.bottomright = ((WIDTH, HEIGHT))

    def load_life(self):
        self.width = 160
        self.height = 128
        backlife, frontlife = self.image_manager.get_hud_images()
        self.backlife_sprite = backlife
        self.frontlife_sprite = frontlife
        self.frontlife_sprite.set_colorkey((0, 1, 0))
        image = pg.Surface((self.width, self.height))
        image.blit(self.backlife_sprite, (0, 0))
        image.blit(self.frontlife_sprite, (0, 0))
        image.set_colorkey((BLACK))
        return image

    def get_life(self, n):
        self.image.fill((WHITE))
        self.image.blit(self.backlife_sprite, (0, 0))
        self.image.blit(self.frontlife_sprite, (0, self.height * n), (0, self.height * n, self.width, self.height))
