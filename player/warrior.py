import pygame as pg
from player import playerstate
import settings

class Warrior(playerstate.Player):
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
        self.buff()
        super().update(dt)

    def buff(self):
        self.clock.tick(FPS)
        if self.totalhealth != self.basehealth:
            self.buffs["Fire"] -= self.clock.get_time() / 1000
            if self.buffs["Fire"] <= 0:
                self.totalhealth = self.basehealth
        if self.damage != self.basedamage:
            self.buffs["Lightning"] -= self.clock.get_time() / 1000
            if self.buffs["Lightning"] <= 0:
                self.damage = self.basedamage
        if self.defense != self.basedefense:
            self.buffs["Fire"] -= self.clock.get_time() / 1000
            if self.buffs["Fire"] <= 0:
                self.defense = self.basedefense

class Fire(playerstate.Fire):
    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]) - 1:
            self.player.totalhealth = self.player.basehealth + self.bonus
            self.player.buffs[self.__class__.__name__] += self.duration
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")

class Lightning(playerstate.Lightning):
    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]):
            self.player.damage = self.player.basedamage + self.bonus
            self.player.buffs[self.__class__.__name__] += self.duration
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")

class Smoke(playerstate.Smoke):
    def update(self, dt):
        super().update(dt)
        if self.current_frame == len(self.image_manager.player[self.__class__.__name__][self.direction]):
            self.player.defense = self.player.basedefense + self.bonus
            self.player.buffs[self.__class__.__name__] += self.duration
            self.player.currentmana -= self.manacost
            n = 1 - self.game.player.currentmana/self.game.player.totalmana
            self.game.hud.update(n, "Mana")
