import pygame as pg
from tile import *
from pytmx import load_pygame
import spritesheet


class UI:
    def __init__(self, directory, player, game):
        pg.init()
        pg.display.init()
        self.game = game
        self.player = player
        self.tmx_data = load_pygame(directory)
        self.display_surface = pg.display.get_surface()
        self.menu_sprites = pg.sprite.Group()
        self.undermenu_sprites = pg.sprite.Group()
        self.button_sprites = pg.sprite.Group()
        self.indicator_sprites = pg.sprite.Group()

        self.createUI()

    def run(self):
        self.menu_sprites.update()
        self.undermenu_sprites.update()
        self.button_sprites.update()
        self.indicator_sprites.update()

        self.undermenu_sprites.draw(self.display_surface)
        self.menu_sprites.draw(self.display_surface)
        self.button_sprites.draw(self.display_surface)
        self.indicator_sprites.draw(self.display_surface)

    def createUI(self):
        for layer in self.tmx_data.layers:
            indicator_list = {'Indicators'}
            menu_list = {'Menus'}
            button_list = {'Buttons'}
            undermenu_list = {'UnderMenus'}
            for x, y, surf in layer.tiles():
                pos = (x * 16, y * 16)
                if layer.name in undermenu_list:
                    Tile(pos, self.undermenu_sprites, None, surf)
                elif layer.name in menu_list:
                    Tile(pos, self.menu_sprites, None, surf)
                elif layer.name in button_list:
                    Tile(pos, self.button_sprites, None, surf)
                elif layer.name in indicator_list:
                    Tile(pos, self.indicator_sprites, None, surf)


class Customization:
    def __init__(self, directory, player, game):
        pg.init()
        pg.display.init()
        self.game = game
        self.click_sound = pg.mixer.Sound('audio/button/ButtonClick.wav')
        self.error_sound = pg.mixer.Sound('audio/button/ButtonClickError.wav')
        self.player = player



        self.tmx_data = load_pygame(directory)
        self.display_surface = pg.display.get_surface()
        self.frame_sprites = pg.sprite.Group()
        self.text_sprites = pg.sprite.Group()
        self.ui_button_sprites = pg.sprite.Group()
        self.play_button_sprites = pg.sprite.Group()
        self.player_sprite = pg.sprite.GroupSingle()
        self.player_sprite.add(self.player)

        self.skinL = UIButton('left', (500,260), self.click_sound, self.error_sound, self.player, 'skin')
        self.skinR = UIButton('right', (735, 260), self.click_sound, self.error_sound, self.player, 'skin')
        self.hairL = UIButton('left', (500, 325), self.click_sound, self.error_sound, self.player, 'hair')
        self.hairR = UIButton('right', (735, 325), self.click_sound, self.error_sound, self.player, 'hair')
        self.colorL = UIButton('left', (500, 390), self.click_sound, self.error_sound, self.player, 'color')
        self.colorR = UIButton('right', (735, 390), self.click_sound, self.error_sound, self.player, 'color')
        self.eyesL = UIButton('left', (500, 455), self.click_sound, self.error_sound, self.player, 'eyes')
        self.eyesR = UIButton('right', (735, 455), self.click_sound, self.error_sound, self.player, 'eyes')
        self.clothesL = UIButton('left', (500, 520), self.click_sound, self.error_sound, self.player, 'clothes')
        self.clothesR = UIButton('right', (735, 520), self.click_sound, self.error_sound, self.player, 'clothes')
        self.ui_button_sprites.add(self.skinL)
        self.ui_button_sprites.add(self.skinR)
        self.ui_button_sprites.add(self.hairL)
        self.ui_button_sprites.add(self.hairR)
        self.ui_button_sprites.add(self.colorL)
        self.ui_button_sprites.add(self.colorR)
        self.ui_button_sprites.add(self.eyesL)
        self.ui_button_sprites.add(self.eyesR)
        self.ui_button_sprites.add(self.clothesL)
        self.ui_button_sprites.add(self.clothesR)
        self.createUI()

    def run(self):
        self.frame_sprites.update()
        self.text_sprites.update()
        self.play_button_sprites.update()
        self.player.update()
        self.ui_button_sprites.update()

        self.frame_sprites.draw(self.display_surface)
        self.play_button_sprites.draw(self.display_surface)
        self.text_sprites.draw(self.display_surface)
        self.player_sprite.draw(self.display_surface)
        self.ui_button_sprites.draw(self.display_surface)

        for sprite in self.play_button_sprites:
            mouse_pos = pg.mouse.get_pos()
            if sprite.rect.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    self.player.can_move = True
                    self.player.scale = 64
                    self.player.hitbox.topleft = (700,500)
                    self.player.load_assets()
                    self.game.set_state('Game')


    def createUI(self):
        for layer in self.tmx_data.layers:
            frame_list = {'Frames'}
            text_list = {'Text'}
            play_button_list = {'Play Button'}
            for x, y, surf in layer.tiles():
                pos = (x * 16, y * 16)
                if layer.name in frame_list:
                    Tile(pos, self.frame_sprites, None, surf)
                elif layer.name in text_list:
                    Tile(pos, self.text_sprites, None, surf)
                elif layer.name in play_button_list:
                    Tile(pos, self.play_button_sprites, None, surf)


class UIButton(pg.sprite.Sprite):
    def __init__(self, direction, pos, click_sound, error_sound, player, attribute):
        super().__init__()
        self.up = True
        self.hover = False
        self.down = False
        self.clicked = False
        self.player = player
        self.attribute = attribute
        self.click_sound = click_sound
        self.error_sound = error_sound
        if direction == 'left':
            self.up_img = pg.image.load('imgs/buttons/left-up.png')
            self.hover_img = pg.image.load('imgs/buttons/left-hover.png')
            self.down_img = pg.image.load('imgs/buttons/left-down.png')
            self.incrementor = -1
        else:
            self.up_img = pg.image.load('imgs/buttons/right-up.png')
            self.hover_img = pg.image.load('imgs/buttons/right-hover.png')
            self.down_img = pg.image.load('imgs/buttons/right-down.png')
            self.incrementor = 1

        self.image = self.up_img
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.collisions()
        if self.up:
            self.image = self.up_img
        elif self.hover:
            self.image = self.hover_img
        elif self.down:
            self.image = self.down_img

    def collisions(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.up = False
            self.hover = True
            if pg.mouse.get_pressed()[0] and not self.clicked:
                self.hover = False
                self.down = True
                self.clicked = True
                if self.player.set_image(self.attribute, self.incrementor):
                    pg.mixer.Sound.play(self.click_sound)
                else:
                    pg.mixer.Sound.play(self.error_sound)
            elif not pg.mouse.get_pressed()[0]:
                self.down = False
                self.clicked = False
        else:
            self.up = True
            self.hover = False
            self.down = False
            self.clicked = False



