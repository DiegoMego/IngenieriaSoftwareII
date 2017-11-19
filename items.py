import pygame as pg
from imagemanager import *

class Item:
    def __init__(self, ID, width, height):
        self.ID = ID
        self.width = width
        self.height = height

class Bag(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.bags
        super().__init__(self.groups)
        imagemanager = ImageManager.get_instance()
        self.image = imagemanager.bag
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.generator = self.animate()
        self.done = False

    def animate(self):
        for y in range(0, 4):
            yield -5
        for y in range(0, 4):
            yield 4

    def events(self):
        pass

    def update(self):
        if not self.done:
            try:
                self.rect.y += next(self.generator)
            except Exception as e:
                self.done = True
