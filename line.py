import pygame as pg

class Line(pg.sprite.Sprite):
    def __init__(self, game, x1, y1, x2, y2, inverted = False):
        self.groups = game.lines
        super().__init__(self.groups)
        self.points = []
        self.width = x2 - x1
        y = y1
        if inverted:
            y = y2
        self.height = abs(y2 - y1)
        self.rect = pg.Rect(x1, y, self.width, self.height)
        self.hit_rect = self.rect
        self.x = x1
        self.y = y
        self.rect.x = x1
        self.rect.y = y
        self.get_points(x1, y1, x2, y2)

    def get_points(self, x1, y1, x2, y2):
        x_1 = int(x1)
        x_2 = int(x2)
        y_1 = int(y1)
        y_2 = int(y2)
        try:
            m = (y_2 - y_1) / (x_2 - x_1)
        except ZeroDivisionError as e:
            m = ""
        if m:
            b = y_1 - m * x_1
            for i in range(x_1, x_2 + 1):
                self.points.append([i, m * i + b])

    def check_collision(self, sprite, axis):
        if axis == "x":
            for point in self.points:
                if sprite.hit_rect.collidepoint(point[0], point[1]):
                    if point[0] > sprite.hit_rect.centerx:
                        sprite.pos.x = point[0] - sprite.hit_rect.width / 2
                    if point[0] < sprite.hit_rect.centerx:
                        sprite.pos.x = point[0] + sprite.hit_rect.width / 2
                    #sprite.vel.x = 0
                    sprite.hit_rect.centerx = sprite.pos.x

        if axis == "y":
            for point in self.points:
                if sprite.hit_rect.collidepoint(point[0], point[1]):
                    if point[1] > sprite.hit_rect.centery:
                        sprite.pos.y = point[1] - sprite.hit_rect.height / 2
                    if point[1] < sprite.hit_rect.centery:
                        sprite.pos.y = point[1] + sprite.hit_rect.height / 2
                    #sprite.vel.y = 0
                    sprite.hit_rect.centery = sprite.pos.y
