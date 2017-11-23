import pygame as pg
import effects
from imagemanager import *

class FlareRed(effects.Effect):
    def __init__(self, game, pos, direction, damage):
        super(). __init__(game, pos, direction, damage)
