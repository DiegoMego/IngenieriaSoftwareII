import pygame as pg
from settings import *

class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILEWIDTH, TILEHEIGHT))
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILEWIDTH
        self.rect.y = y * TILEHEIGHT
        self.hit_rect = self.rect

    def events(self):
        pass

    def update(self):
        pass

# class Fence:
#     def __init__(self, x, y, width, height):
#         self.image_manager = ImageManager.get_instance()
#         self.x = x
#         self.y = y
#         self.width = 160
#         self.height = 320
#         self.angle = 30
#
#     def load_image(self, i_start, i_end):
#         image = pg.Surface((160 ))
#         for i in range(i_start, i_end + 1):
