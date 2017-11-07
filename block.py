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

class Fence:
    def __init__(self, act, x, y):
        self.image_manager = ImageManager.get_instance()
        self.act = act
        self.x = x
        self.y = y
        self.width = 160
        self.height = 320
        self.offset_x = 80
        self.offset_y = 40

    def load_image(self, i_start, i_end):
        image = pg.Surface((self.width + (i_end - i_start) * self.offset_x, self.height + (i_end - i_start) * self.offset_y))
        for i in range(i_end, i_start - 1, -1):
            image.blit(self.image_manager.objects[self.act][i], ((i_end - i) * (self.width - self.offset_x), (i_end - i) * (self.height - self.offset_y)))
        return image
