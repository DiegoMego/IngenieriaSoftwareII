import pygame as pg
from effects import effect

class FlareWhite(effect.Effect):
    def __init__(self, game, pos, direction, damage):
        super(). __init__(game, pos, direction, damage)