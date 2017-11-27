import pygame as pg
import math
import settings
import pytmx
vec = pg.math.Vector2

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface, objects_surface, generator):
        i = 0
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    #tile = temp_tile.convert_alpha()
                    try:
                        tile.set_colorkey(settings.FUCHSIA)
                    except Exception as e:
                        pass
                    if tile:
                        #tile.set_alpha(100)
                        i += 1
                        next(generator)
                        if layer.name == "B_1" or layer.name == "B_2":
                            surface.blit(tile, (x * self.tmxdata.tilewidth + layer.offsetx, y * self.tmxdata.tileheight + layer.offsety))
                        else:
                            objects_surface.blit(tile, (x * self.tmxdata.tilewidth + layer.offsetx, y * self.tmxdata.tileheight + layer.offsety))
        #print(i)

    def make_map(self, generator):
        temp_surface = pg.Surface((self.width, self.height))
        objects_surface = pg.Surface((self.width, self.height))
        objects_surface.set_colorkey(settings.BLACK)
        self.render(temp_surface, objects_surface, generator)
        return temp_surface, objects_surface

class Camera:
    def __init__(self, width, height):
        self.pos = vec(0, 0)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.pos)

    def apply_rect(self, rect):
        return rect.move(self.pos)

    def update(self, target):
        x = -target.rect.centerx + int(settings.WIDTH / 2)
        y = -target.rect.centery + int(settings.HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - settings.WIDTH), x)
        y = max(-(self.height - settings.HEIGHT), y)
        self.pos.x = x
        self.pos.y = y

    def onscreen(self, entity):
        if -self.pos.x < entity.rect.x < (-self.pos.x + settings.WIDTH) and -self.pos.y < entity.rect.y < (-self.pos.y + settings.HEIGHT):
            return True
        return False

    def inside(self):
        row = math.floor(-self.pos.y / settings.TILEHEIGHT)
        col = math.floor(-self.pos.x / settings.TILEWIDTH)
        return row, col

# class Map:
#     def __init__(self, filename):
#         self.data = []
#         self.saved_data = []
#         with open(filename, "rt") as f:
#             for line in f:
#                 self.data.append(list(line.strip()))
#
#         self.tilewidth = len(self.data[0])
#         self.tileheight = len(self.data)
#         self.width = self.tilewidth * TILEWIDTH
#         self.height = self.tileheight * TILEHEIGHT
#
#     def update(self, row, col, mod = "."):
#         if mod != ".":
#             self.saved_data.remove((mod, row, col))
#             self.data[row].pop(col)
#         else:
#             self.saved_data.append((self.data[row].pop(col), row, col))
#         self.data[row].insert(col, mod)
#
#     def find_player(self):
#         for row, tiles in enumerate(self.data):
#             for col, tile in enumerate(tiles):
#                 if tile == PLAYER_LETTER:
#                     return col, row
