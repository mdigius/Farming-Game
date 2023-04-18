import pygame as pg


from settings import *
from tile import *
import helper
from pytmx import load_pygame




class Map:
    def __init__(self, directory, start_pos, player, game):
        pg.init()
        pg.display.init()
        self.game = game
        self.player = player
        self.start_pos = start_pos
        self.directory = directory
        self.tmx_data = load_pygame(directory)
        self.display_surface = pg.display.get_surface()
        self.door_sprites = NoSortCameraGroup()
        self.visible_sprites = YSortCameraGroup()
        self.visible_sprites.add(self.player)
        self.background_sprites = NoSortCameraGroup()
        self.ground_sprites = NoSortCameraGroup()
        self.obstacles_sprites = YSortCameraGroup()
        self.createMap()
        self.player.set_map_info(self.obstacles_sprites)

    def run(self):
        self.background_sprites.update()
        self.ground_sprites.update()
        self.visible_sprites.update()
        self.obstacles_sprites.update()
        self.door_sprites.update(self.player)


        self.background_sprites.custom_draw(self.player)
        self.ground_sprites.custom_draw(self.player)
        self.obstacles_sprites.custom_draw(self.player)
        self.door_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)


    def createMap(self):
        for layer in self.tmx_data.layers:

            ground_list = {'Ground', 'Grass', 'Walkthrough objects', 'Ponds', 'Floor'}
            object_list = {'Objects', 'Buildings', 'Walls', "Wall Top", "Dresser"}
            door_list = ['Doors', "Greenhouse Door"]
            background_list = {'Water'}
            animatable_object_list = {'Animatable Objects', 'Animatable Water'}
            for x, y, surf in layer.tiles():
                pos = (x * 48, y * 48)
                for gid, props in self.tmx_data.tile_properties.items():
                    if surf == self.tmx_data.get_tile_image_by_gid(props['frames'][0].gid):
                        animations = []
                        for picture in props['frames']:
                            surf = self.tmx_data.get_tile_image_by_gid(picture.gid)
                            surf = pg.transform.scale(surf, (48, 48))
                            animations.append(surf)
                        if layer.name in animatable_object_list:
                            Tile(pos, [self.visible_sprites, self.obstacles_sprites], animations, surf)
                    else:
                        surf2 = pg.transform.scale(surf, (48, 48))
                        if layer.name in ground_list:
                            Tile(pos, self.ground_sprites, None, surf2)
                        elif layer.name in object_list:
                            Tile(pos, [self.visible_sprites, self.obstacles_sprites], None, surf2)
                        elif layer.name in background_list:
                            Tile(pos, self.background_sprites, None, surf2)
                        elif layer.name in door_list:
                            Door(pos, [self.door_sprites], surf2, layer.name, self.game)










class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class NoSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
