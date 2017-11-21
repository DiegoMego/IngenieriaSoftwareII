import pygame as pg
import playerstate
from effects import *
from settings import *

class Sorcerer(playerstate.Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

    def load_data(self):
        super().load_data()
        self.states["Fire"] = Fire(self)
        self.states["Lightning"] = Lightning(self)
        self.states["Smoke"] = Smoke(self)
        self.clock = pg.time.Clock()
        self.buffs = {"Fire": 0,
                      "Lightning": 0,
                      "Smoke": 0}

    def update(self, dt):
        super().update(dt)

class Fire(playerstate.Fire):
    def __init__(self, player):
        super().__init__(player)
        self.damage = 100

    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]) - 1:
            FlareRed(self.game, self.player.pos, self.direction, self.damage)
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")

class Lightning(playerstate.Lightning):
    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]):
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")

class Smoke(playerstate.Smoke):
    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]):
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")
