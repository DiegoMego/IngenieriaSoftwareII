import pygame as pg
from settings import *
from imagemanager import *
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
        self.hit_rect = copy.copy(MOB_HIT_RECT)
        self.classname = "Felltwin"
        self.images_path = path.join(path.join(MOB_FOLDER, self.classname), MOB_FILETYPE % (self.classname))
        self.x = x
        self.y = y
        self.pos = vec(x, y) * TILESIZE
        self.image_offset_x, self.image_offset_y = 0, -20
        self.image_size = 128
        self.images = []
        self.load_data()
        self.load_attributes()

    def load_data(self):
        self.states = {"Idle": Idle(self),
                       "Walk": Walk(self),
                       "Attack": Attack(self),
                       "GetHit": GetHit(self),
                       "Die": Die(self)}

        self.player_in_range = False
        self.current_frame = 0
        self.last_update = 0
        self.direction = "down"
        self.state_name = "Idle"
        self.state = self.states[self.state_name]
        self.images_loaded = False

    def load_attributes(self):
        self.health = Health(self.rect.width, 7)
        self.totalhealth = 200
        self.currenthealth = 200
        self.previoushealth = 200
        self.damage = 10
        self.hit_rate = 100
        self.defense = 50
        self.level = 1

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.images_loaded = False
        self.current_frame = 0
        self.state.done[state_name] = False
        self.state_name = state_name
        self.state = self.states[self.state_name]

    def events(self):
        self.state.events()

    def update(self):
        for key, value in self.state.done.items():
            if value:
                self.flip_state(key)

        self.state.update()
        self.rect.center = self.hit_rect.center
        self.animate()

    def player_detected(self):
        if self.pos.distance_to(self.game.player.state.pos) < 400:
            self.player_in_range = True
        if self.pos.distance_to(self.game.player.pos) > 1000:
            self.player_in_range = False

    def gets_hit(self):
        if self.previoushealth > self.currenthealth:
            self.previoushealth = self.currenthealth
            return True
        return False

    def draw_health(self):
        ratio = self.currenthealth / self.totalhealth
        width = int(self.rect.width * ratio)
        self.health.set_width(width, 7)
        self.health.set_pos(self.rect.x, self.rect.y)
        self.health.get_color(ratio)
        self.game.screen.blit(self.health.image, self.game.camera.apply(self.health))

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

class MobState:
    def __init__(self, mob):
        pg.sprite.Sprite.__init__(self)
        self.keyhandler = KeyHandler()
        self.image_manager = ImageManager.get_instance()
        self.game = mob.game
        self.mob = mob
        self.pos = vec(mob.x, mob.y) * TILESIZE

    def load_data(self):
        pass

    def isdead(self):
        if self.mob.currenthealth <= 0:
            self.mob.previoushealth = self.mob.currenthealth
            return True
        return False

    def events(self):
        pass

    def update(self):
        pass

class Idle(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False,
                     "Die": False}

        self.mob.image = self.image_manager.get_image(self.mob.images_path, 1409, 1045, self.mob.image_size, self.mob.image_size)
        self.mob.rect = self.mob.image.get_rect()

    def load_images(self):
        self.mob.images.clear()
        index = self.keyhandler.vel_directions[self.mob.direction][0]
        x_start = 1409
        x_end = 3073
        y = 1045 + (self.mob.image_size + 1) * index
        image_list = self.image_manager.load_images(self.mob.images_path, x_start, x_end, y, self.mob.image_size, self.mob.image_size)
        self.mob.images = self.image_manager.format_images(image_list, self.mob.image_offset_x, self.mob.image_offset_y)

    def events(self):
        if self.isdead():
            self.done["Die"] = True
        elif self.ishit():
            self.done["GetHit"] = True
        elif self.mob.player_in_range or (self.mob.current_frame + 1) % len(self.mob.images) == 0:
            self.done["Walk"] = True

    def update(self):
        if not self.mob.images_loaded:
            self.mob.images_loaded = True
            self.load_images()

class Walk(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False,
                     "Attack": False,
                     "GetHit": False,
                     "Die": False}

    def load_images(self):
        self.mob.images.clear()
        self.random_direction = self.keyhandler.get_key(random.randint(0, 7))
        self.distance = 0
        index = self.keyhandler.vel_directions[self.mob.direction][0]
        x_start = 3074
        x_end = 4738
        y = 1045 + (self.mob.image_size + 1) * index
        image_list = self.image_manager.load_images(self.mob.images_path, x_start, x_end, y, self.mob.image_size, self.mob.image_size)
        self.mob.images = self.image_manager.format_images(image_list, self.mob.image_offset_x, self.mob.image_offset_y)

    def follow(self):
        direction = ""
        distance_vector = (self.game.player.pos - self.mob.pos)
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
        self.mob.vel = distance_vector * MOB_SPEED

        return direction

    def events(self):
        if self.mob.isdead():
            self.done["Die"] = True
        elif self.mob.gets_hit():
            self.done["GetHit"] = True
        elif collide_hit_rect(self.mob, self.game.player):
            self.done["Attack"] = True
        elif self.distance >= 160 and not self.mob.player_in_range:
            self.done["Idle"] = True

    def update(self):
        self.mob.vel = vec(0, 0)
        self.previous_direction = self.mob.direction
        if not self.mob.player_in_range:
            self.mob.direction = self.random_direction
            self.vel.x += self.keyhandler.vel_directions[self.random_direction][1] * MOB_SPEED
            self.vel.y += self.keyhandler.vel_directions[self.random_direction][2] * MOB_SPEED
            self.distance += MOB_SPEED
        else:
            self.mob.direction = self.follow()

        if self.vel.x != 0 and self.vel.y != 0:
            self.distance *= 1.4142
            self.vel *= 0.7071

        if self.previous_direction != self.mob.direction:
            self.mob.images_loaded = False

        if not self.mob.images_loaded:
            self.mob.images_loaded = True
            self.load_images()

        self.mob.pos.x += round(self.mob.vel.x, 0)
        self.mob.pos.y += round(self.mob.vel.y, 0)
        self.mob.hit_rect.centerx = self.mob.pos.x
        detect_collision(self.mob, self.game.mob_sprites, "x")
        self.mob.hit_rect.centery = self.mob.pos.y
        detect_collision(self.mob, self.game.mob_sprites, "y")

class Attack(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False,
                     "Walk": False,
                     "GetHit": False,
                     "Die": False}

    def load_images(self):
        self.mob.images.clear()
        index = self.keyhandler.vel_directions[self.mob.direction][0]
        x_start = 0
        x_end = 1920
        y = 7 + (self.mob.image_size + 1) * index
        image_list = self.image_manager.load_images(self.mob.images_path, x_start, x_end, y, self.mob.image_size, self.mob.image_size)
        self.mob.images = self.image_manager.format_images(image_list, self.mob.image_offset_x, self.mob.image_offset_y)

    def apply_damage(self):
        if not self.try_hit:
            self.try_hit = True
            if hit(self.mob.hit_rate, self.game.player.defense, self.mob.level, self.game.player.level):
                self.game.player.currenthealth -= self.mob.damage
                n = 1 - self.game.player.currenthealth/self.game.player.totalhealth
                self.game.hud.get_life(n)

    def events(self):
        if self.isdead():
            self.done["Die"] = True
        elif self.ishit():
            self.done["GetHit"] = True
        elif (self.current_frame + 1) % len(self.action_images[self.direction]) == 0 and not self.mob.player_in_range:
            self.done["Idle"] = True

    def update(self):
        if not self.mob.images_loaded:
            self.mob.images_loaded = True
            self.load_images()
        if self.current_frame == 0:
            self.try_hit = False
        if self.current_frame == 10:
            self.apply_damage()

class GetHit(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.done = {"Idle": False}

    def start_up(self, persistence):
        self.action_images = None
        self.action_images = self.load_images(0, 1408, 1045, 128, 128)
        self.persistence = persistence
        self.current_frame = 0
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def load_images(self):
        self.mob.images.clear()
        index = self.keyhandler.vel_directions[self.mob.direction][0]
        x_start = 0
        x_end = 1408
        y = 1045 + (self.mob.image_size + 1) * index
        image_list = self.image_manager.load_images(self.mob.images_path, x_start, x_end, y, self.mob.image_size, self.mob.image_size)
        self.mob.images = self.image_manager.format_images(image_list, self.mob.image_offset_x, self.mob.image_offset_y)

    def events(self):
        if (self.current_frame + 1) % len(self.mob.images) == 0:
            self.done["Idle"] = True

    def update(self):
        if not self.mob.images_loaded:
            self.mob.images_loaded = True
            self.load_images()
        if self.mob.gets_hit():
            self.current_frame = 0

class Die(MobState):
    def __init__(self, mob):
        super().__init__(mob)
        self.hit_rect = pg.Surface((0, 0))
        self.done = {"None": None}

    def load_images(self):
        self.mob.images.clear()
        index = self.keyhandler.vel_directions[self.mob.direction][0]
        x_start = 1921
        x_end = 3969
        y = 7 + (self.mob.image_size + 1) * index
        image_list = self.image_manager.load_images(self.mob.images_path, x_start, x_end, y, self.mob.image_size, self.mob.image_size)
        self.mob.images = self.image_manager.format_images(image_list, self.mob.image_offset_x, self.mob.image_offset_y)

    def update(self):
        if not self.mob.images_loaded:
            self.mob.images_loaded = True
            self.load_images()
        if self.current_frame == len(self.action_images[self.direction]) - 1:
            self.mob.remove(self.mob.groups)
            self.mob.add(self.game.dead_sprites)

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
