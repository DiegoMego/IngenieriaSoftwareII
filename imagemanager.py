import pygame as pg
import sys
from spritesheet import *
from os import path
from settings import *

class ImageManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = ImageManager()
        return cls._instance

    def load_hud_images(self):
        spritesheet = pg.image.load(path.join(HUD_FOLDER, "hud.png")).convert()
        self.hud = {"Life": (0, self.get_image(spritesheet, 0, 0, 160, 128), self.get_image(spritesheet, 0, 128, 160, 128)),
                    "Mana": (1, self.get_image(spritesheet, 160, 0, 160, 128), self.get_image(spritesheet, 160, 128, 160, 128))}

    def load_terrain(self, act, part):
        if not hasattr(self, "map"):
            self.map = {"Act_1": {},
                        "Act_2": {},
                        "Act_3": {},
                        "Act_4": {},
                        "Act_5": {}}
        spritesheet = pg.image.load(path.join(path.join(MAP_FOLDER, act), part + ".png")).convert()

    def load_player_images(self, actions, keyhandler):
        self.player = {}
        t = ((10, 8, 16, 6, 21, 10), (0, 1045, 2882, 1045, 0, 7, 4420, 1045, 2049, 7))
        generator = (n for n in t[0])
        positions = (p for p in t[1])
        self.dict_init(self.player, actions, keyhandler.vel_directions)
        spritesheet = pg.image.load(path.join(PLAYER_CLASS_FOLDER, PLAYER_SPRITESHEET_GENERATOR % (PLAYER_CLASS, PLAYER_EQUIPMENT))).convert()
        for action in self.player.values():
            end = next(generator)
            for direction in action.values():
                for i in range(end):
                    direction.append(self.create_surface(128, 128))
        for key, action in self.player.items():
            end = next(positions)
            y = next(positions)
            for direction in action.values():
                x = end
                if key == "Attack":
                    for image in direction:
                        surf = self.get_image(spritesheet, x, y, 128, 128)
                        image.blit(surf, (0, -16))
                        x += 128
                    y += 129
                elif key == "Die":
                    for image in direction:
                        surf = self.get_image(spritesheet, x, y, 128, 96)
                        image.blit(surf, (0, 16))
                        x += 128
                    y += 97
                else:
                    for image in direction:
                        surf = self.get_image(spritesheet, x, y, 96, 96)
                        image.blit(surf, (16, 16))
                        x += 96
                    y += 97

    def load_mob_images(self, mob_type, actions, keyhandler):
        if not hasattr(self, "mob"):
            self.mob = {}
        if mob_type not in self.mob:
            self.mob[mob_type] = {}
            t = ((13, 13, 15, 11, 16), (1049, 1045, 3074, 1045, 0, 7, 0, 1045, 1921, 7))
            generator = (n for n in t[0])
            positions = (p for p in t[1])
            self.dict_init(self.mob[mob_type], actions, keyhandler.vel_directions)
            spritesheet = pg.image.load(path.join(MOB_FOLDER, MOB_FILETYPE % (mob_type)))
            for action in self.mob[mob_type].values():
                n = next(generator)
                for direction in action.values():
                    for i in range(n):
                        direction.append(self.create_surface(128, 128))
            for key, action in self.mob[mob_type].items():
                end = next(positions)
                y = next(positions)
                for direction in action.values():
                    x = end
                    for image in direction:
                        surf = self.get_image(spritesheet, x, y, 128, 128)
                        image.blit(surf, (0, -20))
                        x += 128
                    y += 129

    def create_surface(self, width, height, color = WHITE):
        image = pg.Surface((width, height))
        image.fill(color)
        image.set_colorkey(color)
        return image

    def get_image(self, spritesheet, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(spritesheet, (0, 0), (x, y, width, height))
        return image

    def dict_init(self, d, keys1, keys2):
        for key1 in keys1:
            d[key1] = {}
            for key2 in keys2:
                d[key1][key2] = []

    def loading_screen(self, n, screen):
        bg = pg.image.load(path.join(INTRO_FOLDER, "Loading House.png")).convert()
        screen.blit(bg, (0, 0))
        bar = pg.Surface((674, 37))
        bar.fill(GREEN)
        rect = bar.get_rect()
        for i in range(n):
            screen.blit(bar, (63, 558), (0, 0, rect.width * i / (n - 1), rect.height))
            pg.display.flip()
            yield None
