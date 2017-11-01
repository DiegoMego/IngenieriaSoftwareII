import pygame as pg
import sys
from settings import *

class ImageManager:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = ImageManager()
        return cls.__instance

    def create_surf(self, width = 128, height = 128):
        image = pg.Surface((width, height))
        image.set_colorkey(WHITE)
        return image

    def get_image(self, spritesheet, x, y, width, height):
        image = self.create_surf(width, height)
        image.blit(spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey(WHITE)
        return image

    def load_images(self, spritesheet, x_start, x_end, y, width, height):
        images = []
        for x in range(x_start, x_end, width):
            images.append(self.get_image(spritesheet, x, y, width, height))
        return images

    def format_images(self, imagelist, x, y):
        images = []
        for img in imagelist:
            image = self.create_surf()
            image.blit(img, (x, y))
            images.append(image)
        return images
