import pygame as pg
import copy
from settings import *
from keyhandler import *
from imagemanager import *
from mechanics import *
vec = pg.math.Vector2

class FlareRed(pg.sprite.Sprite):
    def __init__(self, game, pos, direction, damage):
        self.groups = game.effect_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagemanager = ImageManager.get_instance()
        self.pos = vec(pos)
        self.image = self.imagemanager.effects["Shoot"][0]
        self.rect = self.image.get_rect()
        self.hit_rect = copy.copy(EFFECT_RECT)
        self.direction = direction
        self.damage = damage
        keyhandler = KeyHandler.get_instance()
        self.x = keyhandler.vel_directions[self.direction][1]
        self.y = keyhandler.vel_directions[self.direction][2]
        self.explode = False

    def load(self):
        self.states = {"Shoot": Shoot(),
                       "Explode": Explode()}
        self.state_name = "Shoot"
        self.state = self.states[self.state_name]

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.state.done[state_name] = False
        self.state_name = state_name
        self.state = self.states[self.state_name]
        self.state.start_up()

    def events(self):
        self.state.events()

    def update(self, dt):
        for key, value in self.state.done.items():
            if value:
                self.flip_state(key)
        self.state.update(dt)
        self.vel = self.state.vel
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.collide(collide_effect(self, self.game.mob_sprites))
        self.rect.centerx = self.hit_rect.centerx
        self.rect.centery = self.hit_rect.centery - 30
        self.action(self.imagemanager.effects["Shoot"])

    def collide(self, mob_hit):
        if mob_hit:
            self.explode = True

    def action(self, action):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(action)
            self.image = action[self.current_frame]

class State:
    def __init__(self, effect):
        self.effect = effect
        self.last_update = 0
        self.current_frame = 0

    def events(self):
        pass

    def update(self, dt):
        pass

    def action(self, action):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(action)
            self.image = action[self.current_frame]

class Shoot(State):
    def __init__(self, effect):
        super().__init__(effect)
        self.done = {"Explode": False}
        self.clock = pg.time.Clock()
        self.lifetime = 30

    def events(self):
        if self.effect.explode:
            self.done["Explode"] = True

    def update(self, dt):
        self.clock.tick(FPS)
        self.lifetime -= self.clock.get_time() / 1000
        self.vel = vec(0, 0)
        self.vel.x = self.x * MISSILE_SPEED * dt
        self.vel.y = self.y * MISSILE_SPEED * dt
        self.action(self.imagemanager.effects[self.__class__.__name__])

class Explode(State):
    def __init__(self, effect):
        super().__init__(effect)
        self.done = {"None": None}
        self.finish = False

    def events(self):
        pass

    def update(self, dt):
        self.vel = vec(0, 0)
        if not self.finish:
            self.action(self.imagemanager.effects[self.__class__.__name__])
        if self.current_frame == len(self.imagemanager.effects[self.__class__.__name__]):
            pass
