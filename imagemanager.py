import pygame as pg
import sys
from os import path
from settings import *

class ImageManager:
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = ImageManager()
        return cls.__instance

    def get_hud_images(self):
        spritesheet = pg.image.load(path.join(HUD_FOLDER, "Life.png"))
        empty_life = pg.Surface((160, 128))
        full_life = pg.Surface((160, 128))
        empty_life.blit(spritesheet, (0, 0), (0, 0, 160, 128))
        full_life.blit(spritesheet, (0, 0), (0, 128, 160, 128))
        return empty_life, full_life

    def load_player_images(self):
        spritesheet = pg.image.load(path.join(PLAYER_CLASS_FOLDER, PLAYER_SPRITESHEET_GENERATOR % (PLAYER_CLASS, PLAYER_EQUIPMENT))).convert()
        #spritesheet, x_start, x_end, y_start, width, height, image_x, image_y
        self.player_idle = self.create_action_dict(spritesheet, 0, 960, 1045, 96, 96, 16, 16)
        self.player_walk = self.create_action_dict(spritesheet, 2882, 3650, 1045, 96, 96, 16, 16)
        self.player_attack = self.create_action_dict(spritesheet, 0, 2048, 7, 128, 128, 0, -16)
        self.player_gethit = self.create_action_dict(spritesheet, 4420, 4996, 1045, 96, 96, 16, 16)
        self.player_die = self.create_action_dict(spritesheet, 0, 960, 1045, 96, 96, 16, 16)

    def get_image(self, spritesheet, x, y, width, height, img_x = 0, img_y = 0):
        image = pg.Surface((128, 128))
        image.fill(WHITE)
        image.blit(spritesheet, (img_x, img_y), (x, y, width, height))
        image.set_colorkey(WHITE)
        return image

    def create_action_dict(self, spritesheet, x_start, x_end, y_start, width, height, image_x, image_y):
        action_dir = {"down": [],
                      "downleft": [],
                      "left": [],
                      "upleft": [],
                      "up": [],
                      "upright": [],
                      "right": [],
                      "downright": []}

        y = y_start

        for key in action_dir:
            for x in range(x_start, x_end, width):
                action_dir[key].append(self.get_image(spritesheet, x, y, width, height, image_x, image_y))

            y += height + 1

        return action_dir
