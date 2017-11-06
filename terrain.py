import pygame as pg
import os
import math
from settings import *
from spritesheet import *
from imagemanager import *
vec = pg.math.Vector2

class Terrain(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image_manager = ImageManager.get_instance()
        self.acts = ("Act_1", "Act_2", "Act_3", "Act_4", "Act_5")
        self.parts = ("Town", "")
        self.image = self.load_terrain()
        self.rect = self.image.get_rect()

    def load_terrain(self):
        surf = pg.image.load(path.join(IMAGE_FOLDER, "Rogue Encampment.png")).convert()
        # self.image_manager.load_terrain(self.acts[0], self.parts[0])
        # surf = pg.Surface((7840, 3920))
        # basic = self.image_manager.map[self.acts[0]][self.parts[0]][4]
        # halfwidth = int(TILEWIDTH / 2)
        # halfheight = int(TILEHEIGHT / 2)
        # for y in range(-halfheight, 3920 + halfheight, TILEHEIGHT):
        #     for x in range(-halfwidth, 7840 + halfwidth, TILEWIDTH):
        #         surf.blit(basic, (x, y))
        #         surf.blit(basic, (x + halfwidth, y + halfheight))
        return surf
