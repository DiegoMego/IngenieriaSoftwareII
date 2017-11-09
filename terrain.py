import pygame as pg
import os
import math
from settings import *
from imagemanager import *
vec = pg.math.Vector2

class Terrain(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image_manager = ImageManager.get_instance()
        self.image = self.load_terrain()
        self.rect = self.image.get_rect()

    def load_terrain(self):
        surf = pg.image.load(path.join(IMAGE_FOLDER, "Rogue Encampment.png")).convert()
        return surf
