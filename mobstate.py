import pygame as pg
from settings import *
from spritesheet import *
from keyhandler import *
from mechanics import *
import random
import math
import copy
vec = pg.math.Vector2

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.hit_rect = copy.copy(MOB_HIT_RECT)
        self.load_data()
        self.load_attributes()

    def load_data(self):
        self.states = {"Idle": Idle(self),
                       "Walk": Walk(self),
                       "Attack": Attack(self),
                       "GetHit": GetHit(self),
                       "Die": Die(self)}
        self.state_name = "Idle"
        self.state = self.states[self.state_name]
        self.image = self.state.image
        self.rect = self.state.rect
        self.hit_rect.center = self.rect.center

    def load_attributes(self):
        self.health = Health(self.rect.width, 7)
        self.totalhealth = 200
        self.currenthealth = 200
        self.previoushealth = 200
        self.damage = 40
        self.hit_rate = 100
        self.defense = 50
        self.level = 1

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.state.done[state_name] = False
        self.state_name = state_name
        persistent = self.state.persistence
        self.state = self.states[self.state_name]
        self.state.start_up(persistent)

    def update(self):
        for key, value in self.state.done.items():
            if value:
                self.flip_state(key)

        self.state.update()
        self.image = self.state.image
        self.rect = self.state.rect
        self.hit_rect = self.state.hit_rect

    def draw_health(self):
        ratio = self.currenthealth / self.totalhealth
        width = int(self.rect.width * ratio)
        self.health.set_width(width, 7)
        self.health.set_pos(self.rect.x, self.rect.y)
        self.health.get_color(ratio)
        self.game.screen.blit(self.health.image, self.game.camera.apply(self.health))

class MobState(pg.sprite.Sprite):
    def __init__(self, mob):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.keyhandler = KeyHandler.get_instance()
        self.game = mob.game
        self.mob = mob
        self.pos = vec(mob.x, mob.y) * TILESIZE
        self.inbattle = False
        self.mob_class = "Felltwin"
        self.hit_rect = copy.copy(MOB_HIT_RECT)
        self.inital_data()

    def inital_data(self):
        self.current_frame = 0
        self.last_update = 0
        self.direction = "down"
        self.persistence = {"direction": self.direction,
                            "pos": self.pos,
                            "battle": self.inbattle}

    def start_up(self, direction_persistence):
        self.persistence = direction_persistence

    def detect(self):
        if self.pos.distance_to(self.game.player.state.pos) < 400:
            self.inbattle = True

    def gets_hit(self):
        if self.mob.previoushealth > self.mob.currenthealth:
            self.mob.previoushealth = self.mob.currenthealth
            return True
        return False

    def isdead(self):
        if self.mob.currenthealth <= 0:
            self.mob.previoushealth = self.mob.currenthealth
            return True
        return False

    def update(self):
        pass

    def action(self, action_type, action_dir):
        self.last_dir = action_dir
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(action_type[action_dir])
            self.image = action_type[action_dir][self.current_frame]
            self.rect = self.image.get_rect()

class Idle(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False,
                     "Die": False}
        self.image = self.image_manager.mob[self.mob_class][self.__class__.__name__][0]
        self.rect = self.image.get_rect()
        self.hit_rect.center = self.rect.center

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.inbattle = self.persistence["battle"]
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def update(self):
        if self.isdead():
            self.done["Die"] = True
        elif self.gets_hit():
            self.done["GetHit"] = True
        else:
            self.action(self.image_manager.mob[self.mob_class][self.__class__.__name__], self.direction)
            self.hit_rect.centerx = self.pos.x
            self.hit_rect.centery = self.pos.y
            self.rect.center = self.hit_rect.center
            self.detect()
            if self.inbattle == True or (self.current_frame + 1) % len(self.image_manager.mob[self.mob_class][self.__class__.__name__][self.direction]) == 0:
                self.persistence["battle"] = self.inbattle
                self.done["Walk"] = True

class Walk(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False,
                     "Attack": False,
                     "GetHit": False,
                     "Die": False}

    def start_up(self, persistence):
        self.isattacking = False
        self.persistence = persistence
        self.inbattle = self.persistence["battle"]
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]
        self.random_direction = self.keyhandler.get_key(random.randint(0, 7))
        self.distancia = 0

    def follow(self):
        direction = ""
        distance_vector = (self.game.player.state.pos - self.pos)
        distance_vector.x = round(distance_vector.x, 2)
        distance_vector.y = round(distance_vector.y, 2)
        for key, value in self.keyhandler.move_keys.items():
            if distance_vector.y != 0:
                distance_vector.y = math.copysign(1, distance_vector.y)
                direction += key if value[1] == distance_vector.y else ""
        for key, value in self.keyhandler.move_keys.items():
            if distance_vector.x != 0:
                distance_vector.x = math.copysign(1, distance_vector.x)
                direction += key if value[0] == distance_vector.x else ""
        self.vel = distance_vector * MOB_SPEED

        return direction

    def collide_hit_rect(self, one, two):
        if one is two:
            return False
        return one.hit_rect.colliderect(two.hit_rect)

    def detect_collision(self, group, dir):
        # if self.mob.hit_rect.colliderect(self.game.player.hit_rect):
        #     self.isattacking = True

        if dir == "x":
            hits = pg.sprite.spritecollide(self.mob, group, False, self.collide_hit_rect)
            for hit in hits:
                if hit is self.game.player:
                    self.isattacking = True
                if self.vel.x > 0:
                    self.pos.x = hit.hit_rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hit.hit_rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x

        if dir == "y":
            hits = pg.sprite.spritecollide(self.mob, group, False, self.collide_hit_rect)
            for hit in hits:
                if hit is self.game.player:
                    self.isattacking = True
                if self.vel.y > 0:
                    self.pos.y = hit.hit_rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hit.hit_rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        if self.isdead():
            self.done["Die"] = True
        elif self.gets_hit():
            self.done["GetHit"] = True
        else:
            self.detect()
            self.vel = vec(0, 0)
            if not self.inbattle:
                self.direction = self.random_direction
                self.vel.x += self.keyhandler.vel_directions[self.random_direction][0] * MOB_SPEED
                self.vel.y += self.keyhandler.vel_directions[self.random_direction][1] * MOB_SPEED
                self.distancia += MOB_SPEED
            else:
                self.direction = self.follow()

            if self.vel.x != 0 and self.vel.y != 0:
                self.distancia *= 1.4142
                self.vel *= 0.7071

            self.action(self.image_manager.mob[self.mob_class][self.__class__.__name__], self.direction)
            self.pos.x += round(self.vel.x, 0)
            self.pos.y += round(self.vel.y, 0)
            self.hit_rect.centerx = self.pos.x
            self.detect_collision(self.game.all_sprites, "x")
            self.hit_rect.centery = self.pos.y
            self.detect_collision(self.game.all_sprites, "y")
            self.rect.center = self.hit_rect.center

            if self.distancia >= 160 and not self.inbattle:
                self.persistence["direction"] = self.direction
                self.persistence["pos"] = self.pos
                self.done["Idle"] = True
            elif self.isattacking:
                self.persistence["direction"] = self.direction
                self.persistence["pos"] = self.pos
                self.done["Attack"] = True

class Attack(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False,
                     "Walk": False,
                     "GetHit": False,
                     "Die": False}

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.inbattle = self.persistence["battle"]
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def apply_damage(self):
        if not self.try_hit:
            self.try_hit = True
            if hit(self.mob.hit_rate, self.game.player.defense, self.mob.level, self.game.player.level):
                self.game.player.currenthealth -= self.mob.damage
                n = 1 - self.game.player.currenthealth/self.game.player.totalhealth
                self.game.hud.get_life(n)

    def update(self):
        if self.isdead():
            self.done["Die"] = True
        elif self.gets_hit():
            self.done["GetHit"] = True
        else:
            if (self.current_frame + 1) % len(self.image_manager.mob[self.mob_class][self.__class__.__name__][self.direction]) == 0 and self.persistence["pos"].distance_to(self.game.player.state.pos) > 32:
                self.done["Idle"] = True
            if self.current_frame == 0:
                self.try_hit = False
            if self.current_frame == 10:
                self.apply_damage()
            self.action(self.image_manager.mob[self.mob_class][self.__class__.__name__], self.persistence["direction"])
            self.hit_rect.centerx = self.pos.x
            self.hit_rect.centery = self.pos.y
            self.rect.center = self.hit_rect.center

class GetHit(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False}

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def update(self):
        if self.gets_hit():
            self.current_frame = 0
        if (self.current_frame + 1) % len(self.image_manager.mob[self.mob_class][self.__class__.__name__][self.direction]) == 0:
            self.done["Idle"] = True

        self.action(self.image_manager.mob[self.mob_class][self.__class__.__name__], self.direction)
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center

class Die(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.hit_rect = pg.Surface((0, 0))
        self.finish = False
        self.done = {"None": None}

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]
        self.mob.remove(self.mob.groups)
        self.mob.add(self.game.dead_sprites)

    def update(self):
        if not self.finish:
            self.action(self.image_manager.mob[self.mob_class][self.__class__.__name__], self.direction)
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y
        if self.current_frame == len(self.image_manager.mob[self.mob_class][self.__class__.__name__][self.direction]) - 1:
            self.finish = True

class Health:
    def __init__(self, width, height):
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()

    def get_color(self, ratio):
        if ratio > 0.6:
            self.image.fill(GREEN)
        elif ratio > 0.3:
            self.image.fill(YELLOW)
        else:
            self.image.fill(RED)

    def set_width(self, width, height):
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
