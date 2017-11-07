import pygame as pg
import sys
from os import path
from settings import *

class ImageManager:
    __instance = None
    _mob_images = {}

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = ImageManager()
        return cls.__instance

    def get_hud_images(self):
        spritesheet = pg.image.load(path.join(HUD_FOLDER, "hud.png")).convert()
        empty_life = pg.Surface((160, 128))
        full_life = pg.Surface((160, 128))
        empty_life.blit(spritesheet, (0, 0), (0, 0, 160, 128))
        full_life.blit(spritesheet, (0, 0), (0, 128, 160, 128))
        self.hud_images = {"Life": (empty_life, full_life)}
        return empty_life, full_life

    #AÑADIDO:------------------------------------------------------------------------------------------------
    def get_hud_images_mana(self):
        spritesheet = pg.image.load(path.join(HUD_FOLDER, "hud.png")).convert()
        empty_mana = pg.Surface((160, 128))
        full_mana = pg.Surface((160, 128))
        empty_mana.blit(spritesheet, (0, 0), (160, 0, 160, 128))
        full_mana.blit(spritesheet, (0, 0), (160, 128, 160, 128))
        self.hud_images = {"Mana": (empty_mana, full_mana)}
        return empty_mana, full_mana
    #--------------------------------------------------------------------------------------------------------

    def load_objects(self, act, width, y):
        if not hasattr(self, "objects"):
            self.objects = {}
        spritesheet = pg.image.load(path.join(path.join(MAP_FOLDER, act), "Objects.png")).convert()

        images = []
        for x in range(0, width + 1, 160):
            #spritesheet, x, y, width, height, img_x, img_y, color
            images.append(self.get_image(spritesheet, x, y, 160, 320, 0, 0, 160, 320, FUCHSIA))

        self.objects[act] = images

    def load_terrain(self, act, part):
        if not hasattr(self, "map"):
            self.map = {"Act_1": {},
                        "Act_2": {},
                        "Act_3": {},
                        "Act_4": {},
                        "Act_5": {}}
        spritesheet = pg.image.load(path.join(path.join(MAP_FOLDER, act), part + ".png")).convert()
        rect = spritesheet.get_rect()
        images = []
        for y in range(0, rect.height, 80):
            for x in range(0, rect.width, 160):
                #spritesheet, x, y, width, height, img_x, img_y, color
                images.append(self.get_image(spritesheet, x, y, 160, 80, 0, 0, 160, 80, FUCHSIA))

        self.map[act][part] = images

    def load_player_images(self):
        if not hasattr(self, "player"):
            self.player = {}
        self.player["Idle"] = {}
        self.player["Idle"]["down"] = []
        self.player["Idle"]["down"].append(self.create_surface(128, 128, WHITE))
        spritesheet = pg.image.load(path.join(PLAYER_CLASS_FOLDER, PLAYER_SPRITESHEET_GENERATOR % (PLAYER_CLASS, PLAYER_EQUIPMENT))).convert()
        images = []



        #spritesheet, x_start, x_end, y_start, width, height, image_x, image_y
        self.player_idle = self.create_action_dict(spritesheet, 0, 960, 1045, 96, 96, 16, 16)
        self.player_walk = self.create_action_dict(spritesheet, 2882, 3650, 1045, 96, 96, 16, 16)
        self.player_attack = self.create_action_dict(spritesheet, 0, 2048, 7, 128, 128, 0, -16)
        self.player_gethit = self.create_action_dict(spritesheet, 4420, 4996, 1045, 96, 96, 16, 16)
        self.player_die = self.create_action_dict(spritesheet, 0, 960, 1045, 96, 96, 16, 16)

    def load_mob_images(self, mob_type):
        if not hasattr(self, "mob"):
            self.mob = {}
        spritesheet = pg.image.load(path.join(MOB_FOLDER, MOB_FILETYPE % (mob_type)))
        #spritesheet, x_start, x_end, y_start, width, height, image_x, image_y
        self.mob[mob_type] = {"Idle": self.create_action_dict(spritesheet, 1403, 3073, 1045, 128, 128, 0, -20),
                              "Walk": self.create_action_dict(spritesheet, 3074, 4738, 1045, 128, 128, 0, -20),
                              "Attack": self.create_action_dict(spritesheet, 0, 1920, 7, 128, 128, 0, -20),
                              "GetHit": self.create_action_dict(spritesheet, 0, 1408, 1045, 128, 128, 0, -20),
                              "Die": self.create_action_dict(spritesheet, 1921, 3969, 7, 128, 128, 0, -20)}

    def get_image(self, spritesheet, x, y, width, height, img_x = 0, img_y = 0, img_width = 128, img_height = 128, color = WHITE):
        image = pg.Surface((img_width, img_height))
        image.fill(color)
        image.blit(spritesheet, (img_x, img_y), (x, y, width, height))
        image.set_colorkey(color)
        return image

    def create_surface(self, width, height, color = WHITE):
        image = pg.Surface((width, height))
        image.fill(color)
        image.set_colorkey(color)
        return image

    def blit_rect(self, image, x, y, width, height):
        

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
