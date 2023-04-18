import pygame as pg
import sys

import player
from ui import *
from settings import *
from map import *


class Game:
    def __init__(self):
        pg.display.init()
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.player = player.Player((600, 60))
        self.clock = pg.time.Clock()
        self.map = Map('tmx/Home.tmx', (750, 300), self.player, self)
        self.house_map = Map('tmx/Interior.tmx', (750,300), self.player, self)
        self.UI = Customization('tmx/Customize.tmx', self.player, self)
        self.game_state = 'Customization'
        self.run()

    def update(self):
        pg.display.flip()
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')
        self.screen.fill((255, 255, 255))
        self.clock.tick(FPS)
        if self.game_state == 'Customization':
            self.UI.run()
        elif self.game_state == 'Game':
            self.map.run()
        elif self.game_state == 'Doors':
            self.house_map.run()
            print(self.house_map.obstacles_sprites)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.update()
            self.check_events()

    def set_state(self, state):
        self.game_state = state


game = Game()
