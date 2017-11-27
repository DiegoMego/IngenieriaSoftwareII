import pygame as pg
from os import path
import settings

class SpriteSheet:
    _instance = None
    _sprites = {}
    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = SpriteSheet()
        return cls._instance

    @classmethod
    def add_sprite(cls, folder, filename, fit_screen = False):
        try:
            image = pg.image.load(path.join(folder, filename)).convert()
            if fit_screen:
                cls._sprites[filename[:-4]] = pg.transform.scale(image, (settings.WIDTH, settings.HEIGHT))
            else:
                cls._sprites[filename[:-4]] = image
        except Exception as e:
            print("Sprite already loaded")

    @classmethod
    def get_sprite(cls, filename):
        try:
            return cls._sprites[filename]
        except Exception as e:
            print("Sprite not loaded yet")

    def clear_sprites(cls):
        cls._sprites.clear()
