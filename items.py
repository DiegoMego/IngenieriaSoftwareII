import pygame as pg
import imagemanager as im

class Item(pg.sprite.Sprite):
    def __init__(self, game, ID, width, height):
        self.groups = game.inventory_sprites
        super().__init__(self.groups)
        self.ID = ID
        self.width = width
        self.height = height
        self.drag = False

    def update(self):
        mouse = pg.mouse.get_pos()

class Weapon(Item):
    def __init__(self, game, ID, x, y, width, height):
        super().__init__(game, ID, width, height)
        self.image = None
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bag(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.bags
        super().__init__(self.groups)
        imagemanager = im.ImageManager.get_instance()
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
