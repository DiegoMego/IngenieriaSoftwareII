import pygame as pg
import settings
import keyhandler as kh
import imagemanager as im
import mechanics as mechs
import copy
vec = pg.math.Vector2

class Effect(pg.sprite.Sprite):
    def __init__(self, game, pos, direction, damage):
        self.groups = game.effect_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(pos)
        self.hit_rect = copy.copy(settings.EFFECT_RECT)
        self.direction = direction
        self.damage = damage
        self.mob_hit = None
        self.load()

    def load(self):
        self.states = {"Shoot": Shoot(self),
                       "Explosion": Explosion(self)}
        self.state_name = "Shoot"
        self.state = self.states[self.state_name]

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.state.done[state_name] = False
        self.state_name = state_name
        self.state = self.states[self.state_name]
        self.state.startup()

    def events(self):
        self.state.events()

    def update(self, dt):
        for key, value in self.state.done.items():
            if value:
                self.flip_state(key)
        self.state.update(dt)
        self.image = self.state.image
        if not hasattr(self, "rect"):
            self.rect = self.image.get_rect()
        self.vel = self.state.vel
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.collide(mechs.collide_effect(self, self.game.mob_sprites))
        self.rect.centerx = self.hit_rect.centerx
        self.rect.centery = self.hit_rect.centery - 30

    def collide(self, mob_hit):
        if mob_hit:
            self.mob_hit = mob_hit

class State:
    def __init__(self, effect):
        self.imagemanager = im.ImageManager.get_instance()
        self.effect = effect
        self.last_update = 0
        self.current_frame = 0

    def startup(self):
        pass

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
        self.direction = effect.direction
        keyhandler = kh.KeyHandler.get_instance()
        self.x = keyhandler.vel_directions[self.direction][1]
        self.y = keyhandler.vel_directions[self.direction][2]
        self.done = {"Explosion": False}
        self.clock = pg.time.Clock()
        self.lifetime = 10

    def events(self):
        if self.effect.mob_hit:
            self.done["Explosion"] = True
            self.effect.mob_hit.currenthealth -= self.effect.damage
        if self.lifetime <= 0:
            self.effect.kill()

    def update(self, dt):
        self.clock.tick(settings.FPS)
        self.lifetime -= self.clock.get_time() / 1000
        self.vel = vec(0, 0)
        self.vel.x = self.x * settings.MISSILE_SPEED * dt
        self.vel.y = self.y * settings.MISSILE_SPEED * dt
        self.action(self.imagemanager.effects[self.effect.__class__.__name__][self.__class__.__name__])

class Explosion(State):
    def __init__(self, effect):
        super().__init__(effect)
        self.done = {"None": None}
        self.finish = False

    def startup(self):
        pass

    def events(self):
        pass

    def update(self, dt):
        self.vel = vec(0, 0)
        if not self.finish:
            self.action(self.imagemanager.effects[self.effect.__class__.__name__][self.__class__.__name__])
        if self.current_frame == len(self.imagemanager.effects[self.effect.__class__.__name__][self.__class__.__name__]) - 1:
            self.effect.kill()
