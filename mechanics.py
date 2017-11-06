import pygame as pg
import random

def collide_hit_rect(one, two):
    if one != two:
        return one.hit_rect.colliderect(two.hit_rect)
    return False

def detect_collision(target, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(target, group, False, collide_hit_rect)
        for hit in hits:
            if target.vel.x > 0 and hit.hit_rect.centerx - target.hit_rect.centerx > hit.hit_rect.width / 2:
                target.pos.x = hit.hit_rect.left - target.hit_rect.width / 2
            if target.vel.x < 0 and target.hit_rect.centerx - hit.hit_rect.centerx > hit.hit_rect.width / 2:
                target.pos.x = hit.hit_rect.right + target.hit_rect.width / 2
            target.vel.x = 0
            target.hit_rect.centerx = target.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(target, group, False, collide_hit_rect)
        for hit in hits:
            if target.vel.y > 0 and hit.hit_rect.centery - target.hit_rect.centery > hit.hit_rect.height / 2:
                target.pos.y = hit.hit_rect.top - target.hit_rect.height / 2
            if target.vel.y < 0 and target.hit_rect.centery - hit.hit_rect.centery > hit.hit_rect.height / 2:
                target.pos.y = hit.hit_rect.bottom + target.hit_rect.height / 2
            target.vel.y = 0
            target.hit_rect.centery = target.pos.y

def hit(AR, DR, AL, DL):
    n = random.random()
    chance = 2 * (AR/(AR + DR)) * (AL/(AL + DL))
    if chance > 1:
        chance = 1
    if n <= chance:
        return True
    else:
        return False

def block(BR):
    n = random.random()
    if n <= BR:
        return True
    else:
        return False



'''
Abbreviations:
AR = Attacker's Attack Rating
DR = Defender's Defense rating
Alvl = Attacker's level
Dlvl = Defender's level
BR = Block Rate
'''
