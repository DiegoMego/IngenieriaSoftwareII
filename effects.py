import pygame as pg
import copy
from settings import *
from keyhandler import *
vec = pg.math.Vector2

class FlareRed(pg.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self.groups = game.effect_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(pos)
        self.image = None
        self.rect = self.image.get_rect()
        self.hit_rect = copy.copy(EFFECT_RECT)
        self.direction = direction
        keyhandler = KeyHandler.get_instance()
        self.x = keyhandler.vel_directions[self.direction][1]
        self.y = keyhandler.vel_directions[self.direction][2]

    def update(self, dt):
        self.vel = vec(0, 0)
        self.vel.x = self.x * MISSILE_SPEED * dt
        self.vel.y = self.y * MISSILE_SPEED * dt
        self.pos += self.vel
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        collide_effect(self, self.game.mob_sprites)
