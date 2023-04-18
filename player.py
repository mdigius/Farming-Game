import random

import pygame as pg

import spritesheet
from settings import *
import helper


class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.animations = None
        self.create_lists()
        self.skin_index = random.randint(0,7)
        self.hair_index = random.randint(0,13)
        self.clothes_index = random.randint(0,14)
        self.hair_colour_index = 0
        self.hair_x = 0
        self.eyes_index = 0
        self.eyes_x = 0
        self.player_ss = self.skin_list[self.skin_index]
        self.clothes_ss = self.clothes_list[self.clothes_index]
        self.pants_ss = spritesheet.Spritesheet('imgs/player/clothes/pants.png')
        self.hair_ss = self.hair_list[self.hair_index]
        
        self.eyes_ss = spritesheet.Spritesheet('imgs/player/eyes/eyes.png')
        # self.accessories_ss = spritesheet.Spritesheet('imgs/player/acc/glasses_sun.png')
        self.can_move = False
        self.scale = 160
        self.load_assets()
        self.image = pg.transform.scale(self.player_ss.image_at((0, 0, 32, 32), -1), (80, 80))
        self.rect = self.image.get_rect(topleft=pos)
        self.status = 'down'
        self.hitbox = self.rect
        self.direction = pg.math.Vector2()
        self.frame_index = 0
        self.animation_speed = 0.25
        self.speed = 8
    def create_lists(self):
        self.skin_list = [spritesheet.Spritesheet('imgs/player/characters/char1.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char2.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char3.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char4.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char5.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char6.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char7.png'),
                          spritesheet.Spritesheet('imgs/player/characters/char8.png')]

        self.hair_list = [spritesheet.Spritesheet('imgs/player/hair/bob .png'),
                          spritesheet.Spritesheet('imgs/player/hair/braids.png'),
                          spritesheet.Spritesheet('imgs/player/hair/buzzcut.png'),
                          spritesheet.Spritesheet('imgs/player/hair/curly.png'),
                          spritesheet.Spritesheet('imgs/player/hair/emo.png'),
                          spritesheet.Spritesheet('imgs/player/hair/extra_long.png'),
                          spritesheet.Spritesheet('imgs/player/hair/french_curl.png'),
                          spritesheet.Spritesheet('imgs/player/hair/gentleman.png'),
                          spritesheet.Spritesheet('imgs/player/hair/long_straight .png'),
                          spritesheet.Spritesheet('imgs/player/hair/long_straight_skirt.png'),
                          spritesheet.Spritesheet('imgs/player/hair/midiwave.png'),
                          spritesheet.Spritesheet('imgs/player/hair/ponytail .png'),
                          spritesheet.Spritesheet('imgs/player/hair/spacebuns.png'),
                          spritesheet.Spritesheet('imgs/player/hair/wavy.png')]

        self.clothes_list = [spritesheet.Spritesheet('imgs/player/clothes/basic.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/clown.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/dress .png'),
                             spritesheet.Spritesheet('imgs/player/clothes/floral.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/overalls.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/pumpkin.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/sailor.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/sailor_bow.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/skull.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/spaghetti.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/spooky .png'),
                             spritesheet.Spritesheet('imgs/player/clothes/sporty.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/stripe.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/suit.png'),
                             spritesheet.Spritesheet('imgs/player/clothes/witch.png')]
        self.hair_colour_list = []
        for i in range(14):
            self.hair_colour_list.append(i*256)
        self.eyes_colour_list = []
        for i in range(14):
            self.eyes_colour_list.append(i * 256)

    def set_image(self, type, incrementor):
        if type == 'skin':
            trial_index = self.skin_index + incrementor
            if trial_index >= len(self.skin_list) or trial_index < 0:
                return False
            else:
                self.skin_index += incrementor
                self.player_ss = self.skin_list[self.skin_index]
                self.load_assets()
                return True
        elif type == 'hair':
            trial_index = self.hair_index + incrementor
            if trial_index >= len(self.hair_list) or trial_index < 0:
                return False
            else:
                self.hair_index += incrementor
                self.hair_ss = self.hair_list[self.hair_index]
                self.load_assets()
                return True
        elif type == 'color':
            trial_index = self.hair_colour_index + incrementor
            if trial_index >= len(self.hair_colour_list) or trial_index < 0:
                return False
            else:
                self.hair_colour_index += incrementor
                self.hair_x = self.hair_colour_list[self.hair_colour_index]
                self.load_assets()
                return True
        elif type == 'eyes':
            trial_index = self.eyes_index + incrementor
            if trial_index >= len(self.eyes_colour_list) or trial_index < 0:
                return False
            else:
                self.eyes_index += incrementor
                self.eyes_x = self.eyes_colour_list[self.eyes_index]
                self.load_assets()
                return True
        elif type == 'clothes':
            trial_index = self.clothes_index + incrementor
            if trial_index >= len(self.clothes_list) or trial_index < 0:
                return False
            else:
                self.clothes_index += incrementor
                self.clothes_ss = self.clothes_list[self.clothes_index]
                self.load_assets()
                return True




    def set_map_info(self, obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites

    def load_assets(self):
        self.animations = {'down': [], 'up': [], 'right': [], 'left': [],
                           'down_idle': [], 'up_idle': [], 'right_idle': [], 'left_idle': []
                           }
        y = 0
        z = 128
        for animation in self.animations:
            if not 'idle' in animation:
                player_images = self.player_ss.images_at(
                    [(0, y, 32, 32), (32, y, 32, 32), (64, y, 32, 32), (96, y, 32, 32), (128, y, 32, 32), (160, y, 32, 32), (192, y, 32, 32)], colorkey=-1)
                clothing_images = self.clothes_ss.images_at(
                    [(0, y, 32, 32), (32, y, 32, 32), (64, y, 32, 32), (96, y, 32, 32), (128, y, 32, 32), (160, y, 32, 32), (192, y, 32, 32)], colorkey=-1)

                hair_images = self.hair_ss.images_at(
                    [(self.hair_x + 0, y, 32, 32), (self.hair_x + 32, y, 32, 32), (self.hair_x + 64, y, 32, 32),
                     ((self.hair_x + 96), y, 32, 32), (self.hair_x + 128, y, 32, 32), (self.hair_x + 160, y, 32, 32),
                     (self.hair_x + 192, y, 32, 32)], colorkey=-1)
                eyes_images = self.eyes_ss.images_at(
                    [(self.eyes_x + 0, y, 32, 32), (self.eyes_x + 32, y, 32, 32), (self.eyes_x + 64, y, 32, 32),
                     ((self.eyes_x + 96), y, 32, 32), (self.eyes_x + 128, y, 32, 32), (self.eyes_x + 160, y, 32, 32),
                     (self.eyes_x + 192, y, 32, 32)], colorkey=-1)
                pants_images = self.pants_ss.images_at(
                    [(0, y, 32, 32), (32, y, 32, 32), (64, y, 32, 32), (96, y, 32, 32), (128, y, 32, 32), (160, y, 32, 32), (192, y, 32, 32)], colorkey=-1)
                # acc_images = self.accessories_ss.images_at(
                #     [(0, y, 32, 32), (32, y, 32, 32), (64, y, 32, 32), (96, y, 32, 32),
                #      (96, y, 32, 32), (128, y, 32, 32), (160, y, 32, 32), (192, y, 32, 32)], colorkey=-1)
                for index in range(len(player_images)):
                    pImg = pg.transform.scale(player_images[index], (self.scale, self.scale))
                    cImg = pg.transform.scale(clothing_images[index], (self.scale, self.scale))
                    pntImg = pg.transform.scale(pants_images[index], (self.scale, self.scale))
                    hImg = pg.transform.scale(hair_images[index], (self.scale, self.scale))
                    eImg = pg.transform.scale(eyes_images[index], (self.scale, self.scale))
                    # aImg = pg.transform.scale(acc_images[index], (self.scale, self.scale))
                    pImg.blit(cImg, pImg.get_rect())
                    pImg.blit(pntImg, pImg.get_rect())
                    pImg.blit(eImg, eImg.get_rect())
                    pImg.blit(hImg, pImg.get_rect())
                    # pImg.blit(aImg, pImg.get_rect())
                    self.animations[animation].append(pImg)
                y += 32

            else:

                player_images = self.player_ss.images_at(
                    [(0, z, 32, 32), (32, z, 32, 32)], colorkey=-1)
                clothing_images = self.clothes_ss.images_at(
                    [(0, z, 32, 32), (32, z, 32, 32)], colorkey=-1)
                hair_images = self.hair_ss.images_at(
                    [(self.hair_x, z, 32, 32), (self.hair_x + 32, z, 32, 32)], colorkey=-1)
                eyes_images = self.eyes_ss.images_at(
                    [(self.eyes_x, z, 32, 32), (self.eyes_x + 32, z, 32, 32)], colorkey=-1)
                pants_images = self.pants_ss.images_at(
                    [(0, z, 32, 32), (32, z, 32, 32)], colorkey=-1)
                # acc_images = self.accessories_ss.images_at(
                #     [(0, z, 32, 32), (32, z, 32, 32)], colorkey=-1)
                for index in range(len(player_images)):
                    pImg = pg.transform.scale(player_images[index], (self.scale, self.scale))
                    cImg = pg.transform.scale(clothing_images[index], (self.scale, self.scale))
                    pntImg = pg.transform.scale(pants_images[index], (self.scale, self.scale))
                    hImg = pg.transform.scale(hair_images[index], (self.scale, self.scale))
                    eImg = pg.transform.scale(eyes_images[index], (self.scale, self.scale))
                    # aImg = pg.transform.scale(acc_images[index], (self.scale, self.scale))
                    pImg.blit(cImg, pImg.get_rect())
                    pImg.blit(pntImg, pImg.get_rect())
                    pImg.blit(eImg, eImg.get_rect())
                    pImg.blit(hImg, pImg.get_rect())
                    # pImg.blit(aImg, pImg.get_rect())
                    self.animations[animation].append(pImg)
                z += 32

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def collision(self, direction):
        # collision detection method with one argument for vertical and horizontal
        if direction == 'h':
            # checks if there is any collisions with the sprite if it is moving horizontally
            # if so, depending on the direction will move the player to left or right of obstacle
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        # same concept as above but for the vertical collisions
        if direction == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'
                self.frame_index = 0
                self.animation_speed = 0.08
        else:
            self.animation_speed = 0.25

    def move(self):
        if self.can_move:
            if self.direction.magnitude() != 0:
                # normalizes the vector so that its length is always 1
                # avoids issue where speed is greater when moving diagonally
                self.direction.normalize_ip()
            # changes the rect values by the direction vector * speed
            # also calls the collision method to check both vertical and horizontal collisions
            self.hitbox.x += self.direction.x * self.speed
            self.collision('h')
            self.hitbox.y += self.direction.y * self.speed
            self.collision('v')
            self.rect.center = self.hitbox.center
            self.hitbox = self.rect.inflate(-40, -40)

    def input(self):
        # gets the key inputs from the pygame module and stores it in a variable
        keys = pg.key.get_pressed()
        # changes the direction of the player based on the key pressed
        if keys[pg.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pg.K_s]:
            self.direction.y = 1
            self.status = 'down'
            # resets direction to 0 if no key is currently being pressed
        else:
            self.direction.y = 0
        if keys[pg.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        if self.direction.magnitude() != 0:
            # normalizes the vector so that its length is always 1
            # avoids issue where speed is greater when moving diagonally
            self.direction.normalize_ip()
