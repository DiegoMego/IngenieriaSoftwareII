import pygame as pg
import random

def getNextID():
    ID = 0
    for i in iter(int, 0):
        ID += 1
        yield ID

def collide_line(sprite, lines, axis):
    hits = pg.sprite.spritecollide(sprite, lines, False, collide_hit_rect)
    for hit in hits:
        hit.check_collision(sprite, axis)
    # for line in lines:
    #     line.check_collision(sprite, axis)

def collide_hit_rect(one, two):
    if one != two:
        return one.hit_rect.colliderect(two.hit_rect)
    return False

def collide_effect(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.kill()

def detect_collision(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].hit_rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width / 2
            if hits[0].hit_rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].hit_rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height / 2
            if hits[0].hit_rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].hit_rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def hit(AR, DR, AL, DL):
    random_number = random.random()
    chance = 2 * (AR/(AR + DR)) * (AL/(AL + DL))
    if chance > 1:
        chance = 1
    if random_number <= chance:
        return True
    else:
        return False

def block(BR):
    random_number = random.random()
    if random_number <= BR:
        return True
    else:
        return False



'''
Abbreviations:
AR = Attacker's Attack Rating
DR = Defender's Defense rating
AL = Attacker's level
DL = Defender's level
BR = Block Rate
'''
