import pygame as pg
import os
from settings import *
from keyhandler import *
from spritesheet import *
from imagemanager import *
from mechanics import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.hit_rect = PLAYER_HIT_RECT
        self.pos = vec(x, y) * TILESIZE
        self.images = []
        self.keyhandler = KeyHandler.get_instance()
        self.load_data()
        self.load_attributes()

    def load_data(self):
        self.states = {"Idle": Idle(self),
                       "Walk": Walk(self),
                       "Attack": Attack(self),
                       "GetHit": GetHit(self)}

        self.current_frame = 0
        self.last_update = 0
        self.direction = "down"
        self.state_name = "Idle"
        self.state = self.states[self.state_name]
        self.images_loaded = False

    def load_attributes(self):
        self.totalhealth = 500
        self.currenthealth = 500
        self.previoushealth = 500
        self.damage = 40
        self.hit_rate = 100
        self.defense = 75
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
        self.keyhandler.previous_key = self.direction
        self.direction = self.keyhandler.get_move_direction()

        if self.keyhandler.previous_key != self.direction:
            self.images_loaded = False

        self.animate()

    def gets_hit(self):
        if self.previoushealth > self.currenthealth:
            self.previoushealth = self.currenthealth
            return True
        return False

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

class PlayerState:
    def __init__(self, player):
        self.spritesheet = SpriteSheet.get_instance()
        self.spritesheet.add_sprite(player, PLAYER_CLASS_FOLDER, PLAYER_SPRITESHEET_GENERATOR % (PLAYER_CLASS, PLAYER_EQUIPMENT))
        self.game = player.game
        self.player = player
        self.image_manager = ImageManager.get_instance()
        self.keyhandler = KeyHandler.get_instance()
        self.load_data()

    def load_data(self):
        pass

    def events(self):
        pass

    def update(self):
        pass

class Idle(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False}
        self.image_offset_x, self.image_offset_y = 16, 16
        self.image_size = 96
        self.player.image = self.image_manager.get_image(PLAYER_SPRITESHEET, 0, 1045, self.image_size, self.image_size)
        self.player.rect = self.player.image.get_rect()

    def load_images(self):
        self.player.images.clear()
        index = self.keyhandler.vel_directions[self.player.direction][0]
        x_start = 0
        x_end = 960
        y = 1045 + (self.image_size + 1) * index
        image_list = self.image_manager.load_images(self.spritesheet.get_sprite(self.player), x_start, x_end, y, self.image_size, self.image_size)
        self.player.images = self.image_manager.format_images(image_list, self.image_offset_x, self.image_offset_y)

    def events(self):
        keys = pg.key.get_pressed()
        if self.player.gets_hit():
            self.done["GetHit"] = True
        else:
            for key, value in self.keyhandler.move_keys.items():
                if keys[value[2]]:
                    self.keyhandler.insert_key(key)
                    self.done["Walk"] = True
                    return False

            for key, value in self.keyhandler.action_keys.items():
                if keys[value]:
                    self.done["Attack"] = True
                    return False

    def update(self):
        if not self.player.images_loaded:
            self.player.images_loaded = True
            self.load_images()

class Walk(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False,
                     "Attack": False,
                     "GetHit": False}
        self.image_offset_x, self.image_offset_y = 16, 16
        self.image_size = 96
        #self.image = self.game.image_manager.get_image(PLAYER_SPRITESHEET, 2882, 1045, 96, 96)

    def load_images(self):
        self.player.images.clear()
        index = self.keyhandler.vel_directions[self.player.direction][0]
        x_start = 2882
        x_end = 3650
        y = 1045 + (self.image_size + 1) * index
        #ruta, x_start, x_end, y, width, height
        image_list = self.image_manager.load_images(PLAYER_SPRITESHEET, x_start, x_end, y, self.image_size, self.image_size)
        self.player.images = self.image_manager.format_images(image_list, self.image_offset_x, self.image_offset_y)

    def events(self):
        if self.player.gets_hit():
            self.done["GetHit"] = True
        else:
            keys = pg.key.get_pressed()
            if len(self.keyhandler.move_keyspressed) == 0:
                self.done["Idle"] = True
            elif keys[pg.K_q]:
                self.done["Attack"] = True

    def update(self):
        self.player.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        for key, value in self.keyhandler.move_keys.items():
            if keys[value[2]]:
                self.keyhandler.insert_key(key)
                self.player.vel.x += value[0] * PLAYER_SPEED
                self.player.vel.y += value[1] * PLAYER_SPEED
            else:
                self.keyhandler.remove_key(key)

        if self.player.vel.x != 0 and self.player.vel.y != 0:
            self.player.vel *= 0.7071

        self.player.pos.x += round(self.player.vel.x, 0)
        self.player.pos.y += round(self.player.vel.y, 0)
        self.player.hit_rect.centerx = self.player.pos.x
        detect_collision(self.player, self.game.mob_sprites, "x")
        self.player.hit_rect.centery = self.player.pos.y
        detect_collision(self.player, self.game.mob_sprites, "y")

class Attack(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False,
                     "GetHit": False}
        self.image_offset_x, self.image_offset_y = 0, -16
        self.image_size = 128

    def load_images(self):
        self.player.images.clear()
        index = self.keyhandler.vel_directions[self.player.direction][0]
        x_start = 0
        x_end = 2048
        y = 7 + (self.image_size + 1) * index
        image_list = self.image_manager.load_images(PLAYER_SPRITESHEET, x_start, x_end, y, self.image_size, self.image_size)
        self.player.images = self.image_manager.format_images(image_list, self.image_offset_x, self.image_offset_y)

    def check(self, direction, pos, rect):
        if not self.try_hit:
            self.try_hit = True
            posx = pos.x + self.keyhandler.vel_directions[direction][1] * (rect.width / 2 + 1)
            posy = pos.y + self.keyhandler.vel_directions[direction][2] * (rect.height / 2 + 1)
            for mob in self.game.mob_sprites.sprites():
                if mob.hit_rect.collidepoint(posx, posy) and hit(self.player.hit_rate, mob.defense, self.player.level, mob.level):
                    mob.currenthealth -= self.player.damage

    def events(self):
        keys = pg.key.get_pressed()
        if self.player.gets_hit():
            self.done["GetHit"] = True
        else:
            if (self.player.current_frame + 1) % len(self.player.images) == 0:
                for key, value in self.keyhandler.action_keys.items():
                    if not keys[value]:
                        self.done["Idle"] = True

    def update(self):
        if not self.player.images_loaded:
            self.player.images_loaded = True
            self.load_images()
        if self.current_frame == 9:
            self.check(self.player.direction, self.player.pos, self.player.hit_rect)
        if self.current_frame == 0:
            self.try_hit = False

class GetHit(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False}
        self.image_offset_x, self.image_offset_y = 16, 16
        self.image_size = 96

    def load_images(self):
        self.player.images.clear()
        index = self.keyhandler.vel_directions[self.player.direction][0]
        x_start = 4420
        x_end = 4996
        y = 1045 + (self.image_size + 1) * index
        image_list = self.image_manager.load_images(PLAYER_SPRITESHEET, x_start, x_end, y, self.image_size, self.image_size)
        self.player.images = self.image_manager.format_images(image_list, self.image_offset_x, self.image_offset_y)

    def events(self):
        if (self.player.current_frame + 1) % len(self.player.images) == 0:
            self.done["Idle"] = True

    def update(self):
        if not self.player.images_loaded:
            self.player.images_loaded = True
            self.load_images()
        if self.player.gets_hit():
            self.player.current_frame = 0

'''
class IdleTown(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False}
                        #(self, ruta, x, y, width, height)
        self.image = self.game.image_manager.get_image(PLAYER_SPRITESHEET, 961, 1045, 96, 96)
        self.rect = self.image.get_rect()

    def start_up(self, persistence):
        self.player.image_manager.x = 16
        self.player.image_manager.y = 16
        self.persistence = persistence
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def update(self):
        keys = pg.key.get_pressed()
        if self.ishit():
            self.done["GetHit"] = True
        else:
            for key, value in self.keyhandler.move_keys.items():
                if keys[value[2]]:
                    self.done["Walk"] = True

            for key, value in self.keyhandler.action_keys.items():
                if keys[value]:
                    self.done["Attack"] = True

            self.hit_rect.centerx = self.pos.x
            self.hit_rect.centery = self.pos.y
            self.rect.center = self.hit_rect.center
            self.action(self.idletown_images, self.direction)

class TownWalk(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"IdleTown": False,
                     "Attack": False,
                     "GetHit": False}

    def load_data(self):
        #create_action_dic(x_start, x_end, x_increment, y_start, y_increment, width, height, image_x = 16, image_y = 16)
        self.townwalk_images = self.create_action_dict(3651, 4419, 1045, 96, 96)

    def start_up(self, persistence):
        self.persistence = persistence
        self.keyhandler.move_keyspressed = []
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def collide_hit_rect(self, one, two):
        if one != two:
            return one.hit_rect.colliderect(two.hit_rect)

        return False

    def detect_collision(self, group, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, group, False, self.collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    #error is here
                    self.pos.x = hits[0].hit_rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].hit_rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, group, False, self.collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].hit_rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].hit_rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if self.ishit():
            self.done["GetHit"] = True
        else:
            for key, value in self.keyhandler.move_keys.items():
                if keys[value[2]]:
                    self.keyhandler.insert_key(key)
                    self.vel.x += value[0] * PLAYER_SPEED
                    self.vel.y += value[1] * PLAYER_SPEED
                else:
                    self.keyhandler.remove_key(key)

            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071

            if len(self.keyhandler.move_keyspressed) == 0:
                self.persistence["direction"] = self.direction
                self.persistence["pos"] = self.pos
                self.done["IdleTown"] = True
            elif keys[pg.K_q]:
                self.persistence["direction"] = self.direction
                self.persistence["pos"] = self.pos
                self.done["Attack"] = True

            self.keyhandler.previous_key = self.direction
            self.direction = self.keyhandler.get_move_direction()

            self.action(self.townwalk_images, self.direction)

            self.pos.x += round(self.vel.x, 0)
            self.pos.y += round(self.vel.y, 0)
            self.hit_rect.centerx = self.pos.x
            self.detect_collision(self.game.mob_sprites, "x")
            self.hit_rect.centery = self.pos.y
            self.detect_collision(self.game.mob_sprites, "y")
            self.rect.center = self.hit_rect.center
'''
