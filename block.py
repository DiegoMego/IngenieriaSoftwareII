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
