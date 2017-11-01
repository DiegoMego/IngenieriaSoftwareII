import pygame as pg
from os import path
from settings import *

class SpriteSheet:
    _instance = None
    _sprites = {}
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = SpriteSheet()
        return cls._instance

    @classmethod
    def add_sprite(cls, obj, folder, filename, fit_screen = False):
        try:
            image = pg.image.load(path.join(folder, filename)).convert()
            if fit_screen:
                cls._sprites[obj.__class__.__name__] = pg.transform.scale(image, (WIDTH, HEIGHT))
            else:
                cls._sprites[obj.__class__.__name__] = image
        except Exception as e:
            print("Sprite already loaded")

    @classmethod
    def get_sprite(cls, obj):
        try:
            return cls._sprites[obj.__class__.__name__]
        except Exception as e:
            print("Sprite not loaded yet")

    def clear_sprites(cls):
        cls._sprites.clear()


    def get_terrain(self, x, y):
        image = pg.Surface((160, 80))
        image.fill(WHITE)
        image.blit(self.image, (0, 0), (x, y, 160, 80))
        image.set_colorkey(FUCHSIA)
        return image
