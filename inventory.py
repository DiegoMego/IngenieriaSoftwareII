import pygame as pg
from imagemanager import *

class Inventory(pg.sprite.Sprite):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = Inventory()
        return cls._instance

    def make_inventory(self, game):
        groups = game.inventory_sprites
        super().__init__(groups)
        imagemanager = ImageManager.get_instance()
        self.items = {}
        self.space = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.image = imagemanager.inventory
        self.rect = self.image.get_rect()
        self.rect.top = HEIGHT * 0.2
        self.rect.right = WIDTH
        self.on = False

    def find_slot(self, item):
        for row in self.space:
            for col in row:
                if self.space[row][col] == 0:
                    self.addItem(col, row, item)

    def addItem(self, col, row, item):
        self.items[item.id] = (item, col, row)
        self.space[col][row] = item.ID

    def deleteItem(self, item):
        col = self.items[item.id][1]
        row = self.items[item.id][2]
        self.space[col][row] = 0
        del self.items[item.id]
