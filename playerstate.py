import pygame as pg
from settings import *
from keyhandler import *
from spritesheet import *
from mechanics import *
from imagemanager import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.load_data()
        self.load_attributes()

    def load_data(self):
        self.states = {"Idle": Idle(self),
                       "TownWalk": TownWalk(self),
                       "Walk": Walk(self),
                       "Attack": Attack(self),
                       "GetHit": GetHit(self)}

        self.state_name = "Idle"
        self.state = self.states[self.state_name]
        self.image = self.state.image
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        #self.hit_rect.center = self.rect.center

    def load_attributes(self):
        self.totalhealth = 500
        self.currenthealth = 500
        self.previoushealth = 500
        self.damage = 40
        self.hit_rate = 80
        self.defense = 75
        self.level = 1

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.state.done[state_name] = False
        self.state_name = state_name
        persistent = self.state.persistence
        self.state = self.states[self.state_name]
        self.state.start_up(persistent)

    def events(self):
        self.state.events()

    def update(self):
        for key, value in self.state.done.items():
            if value:
                self.flip_state(key)

        self.state.update()
        self.vel = self.state.vel
        self.image = self.state.image
        self.pos.x += round(self.vel.x, 0)
        self.pos.y += round(self.vel.y, 0)
        self.hit_rect.centerx = self.pos.x
        detect_collision(self, self.game.mob_sprites, "x")
        self.hit_rect.centery = self.pos.y
        detect_collision(self, self.game.mob_sprites, "y")
        self.rect.center = self.hit_rect.center

class PlayerState(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image_manager = ImageManager.get_instance()
        self.keyhandler = KeyHandler.get_instance()
        self.game = player.game
        self.player = player
        self.pos = vec(player.x, player.y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.inital_data()

    def inital_data(self):
        self.current_frame = 0
        self.last_update = 0
        self.direction = "down"
        self.persistence = {"direction": self.direction}

    def start_up(self, direction_persistence):
        self.persistence = direction_persistence

    def gets_hit(self):
        if self.player.previoushealth > self.player.currenthealth:
            self.player.previoushealth = self.player.currenthealth
            return True
        return False

    def events(self):
        pass

    def update(self):
        pass

    def action(self, action_type, action_dir):
        self.last_dir = action_dir
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(action_type[action_dir])
            self.image = action_type[action_dir][self.current_frame]

class Idle(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False}
        self.image = self.image_manager.player_idle[self.direction][0]

    def start_up(self, persistence):
        self.persistence = persistence
        self.direction = self.persistence["direction"]

    def events(self):
        keys = pg.key.get_pressed()
        if self.gets_hit():
            self.done["GetHit"] = True
            return False

        for key, value in self.keyhandler.move_keys.items():
            if keys[value[2]]:
                self.done["Walk"] = True
                return False

        for key, value in self.keyhandler.action_keys.items():
            if keys[value]:
                self.done["Attack"] = True
                return False

    def update(self):
        self.vel = vec(0, 0)
        # self.hit_rect.centerx = self.pos.x
        # self.hit_rect.centery = self.pos.y
        # self.rect.center = self.hit_rect.center
        self.action(self.image_manager.player_idle, self.direction)

class IdleTown(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Walk": False,
                     "Attack": False,
                     "GetHit": False}
        self.image = self.idletown_images[self.direction][0]
        self.rect = self.image.get_rect()

    def start_up(self, persistence):
        self.persistence = persistence
        self.direction = self.persistence["direction"]
        self.pos = self.persistence["pos"]

    def update(self):
        keys = pg.key.get_pressed()
        if self.gets_hit():
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
            self.action(self.image_manager.player_idle, self.direction)

class TownWalk(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"IdleTown": False,
                     "Attack": False,
                     "GetHit": False}
        self.image = self.image_manager.player_idle[self.persistence["direction"]][0]
        self.rect = self.image.get_rect()
        self.hit_rect.center = self.rect.center

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
        if self.gets_hit():
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

            self.action(self.image_manager.player_idle, self.direction)

            self.pos.x += round(self.vel.x, 0)
            self.pos.y += round(self.vel.y, 0)
            self.hit_rect.centerx = self.pos.x
            self.detect_collision(self.game.mob_sprites, "x")
            self.hit_rect.centery = self.pos.y
            self.detect_collision(self.game.mob_sprites, "y")
            self.rect.center = self.hit_rect.center

class Walk(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False,
                     "Attack": False,
                     "GetHit": False}
        # self.image = self.image_manager.player_walk[self.persistence["direction"]][0]
        # self.rect = self.image.get_rect()
        # self.hit_rect.center = self.rect.center

    def start_up(self, persistence):
        self.persistence = persistence
        self.keyhandler.move_keyspressed = []
        self.direction = self.persistence["direction"]
        # self.pos = self.persistence["pos"]

    def events(self):
        keys = pg.key.get_pressed()
        if self.gets_hit():
            self.done["GetHit"] = True
        elif len(self.keyhandler.move_keyspressed) == 0:
            self.persistence["direction"] = self.direction
            self.persistence["pos"] = self.pos
            self.done["Idle"] = True
        elif keys[pg.K_q]:
            self.persistence["direction"] = self.direction
            self.persistence["pos"] = self.pos
            self.done["Attack"] = True

    def update(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        for key, value in self.keyhandler.move_keys.items():
            if keys[value[2]]:
                self.keyhandler.insert_key(key)
                self.vel.x += value[0] * PLAYER_SPEED
                self.vel.y += value[1] * PLAYER_SPEED
            else:
                self.keyhandler.remove_key(key)

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

        self.keyhandler.previous_key = self.direction
        self.direction = self.keyhandler.get_move_direction()
        self.action(self.image_manager.player_walk, self.direction)
        # self.pos.x += round(self.vel.x, 0)
        # self.pos.y += round(self.vel.y, 0)
        # self.hit_rect.centerx = self.pos.x
        # detect_collision(self.player, self.game.mob_sprites, "x")
        # self.hit_rect.centery = self.pos.y
        # detect_collision(self.player, self.game.mob_sprites, "y")
        # self.rect.center = self.hit_rect.center

class Attack(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False,
                     "GetHit": False}
        # self.image = self.image_manager.player_attack[self.persistence["direction"]][0]
        # self.rect = self.image.get_rect()

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.direction = self.persistence["direction"]
        # self.pos = self.persistence["pos"]
        # self.hit_rect.centerx = self.pos.x
        # self.hit_rect.centery = self.pos.y
        # self.rect.center = self.hit_rect.center

    def check(self, direction):
        if not self.try_hit:
            self.try_hit = True
            posx = self.pos.x + self.keyhandler.vel_directions[self.direction][0] * (self.hit_rect.width / 2 + 1)
            posy = self.pos.y + self.keyhandler.vel_directions[self.direction][1] * (self.hit_rect.height / 2 + 1)
            for mob in self.game.mob_sprites.sprites():
                if mob.hit_rect.collidepoint(posx, posy) and hit(self.player.hit_rate, mob.defense, self.player.level, mob.level):
                    mob.currenthealth -= self.player.damage

    def events(self):
        keys = pg.key.get_pressed()
        if self.gets_hit():
            self.done["GetHit"] = True
        elif (self.current_frame + 1) % len(self.image_manager.player_attack[self.direction]) == 0:
            for key, value in self.keyhandler.action_keys.items():
                if not keys[value]:
                    self.done["Idle"] = True

    def update(self):
        self.vel = vec(0, 0)
        if self.current_frame == 9:
            self.check(self.direction)
        if self.current_frame == 0:
            self.try_hit = False
        self.action(self.image_manager.player_attack, self.direction)

class GetHit(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self.done = {"Idle": False}
        # self.image = self.image_manager.player_gethit[self.persistence["direction"]][0]
        # self.rect = self.image.get_rect()

    def start_up(self, persistence):
        self.persistence = persistence
        self.current_frame = 0
        self.direction = self.persistence["direction"]
        # self.pos = self.persistence["pos"]
        # self.hit_rect.centerx = self.pos.x
        # self.hit_rect.centery = self.pos.y
        # self.rect.center = self.hit_rect.center

    def events(self):
        if (self.current_frame + 1) % len(self.image_manager.player_gethit[self.direction]) == 0:
            self.done["Idle"] = True

    def update(self):
        self.vel = vec(0, 0)
        if self.gets_hit():
            self.current_frame = 0
        self.action(self.image_manager.player_gethit, self.direction)
