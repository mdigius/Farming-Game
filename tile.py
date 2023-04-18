import pygame as pg
from settings import *
import random


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, animations, image):
        super().__init__(groups)
        self.animations = animations
        self.image = image
        self.animatable = bool(self.animations)
        if self.animatable:
            self.image = self.animations[0]
            self.animation_index = 0
            self.animation_speed = 0.08
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

    def animate(self):
        self.image = self.animations[int(self.animation_index)]
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations):
            self.animation_index = 0

    def update(self):
        if self.animatable:
            self.animate()


class Door(Tile):
    def __init__(self, pos, groups, image, door_name, game):
        super().__init__(pos, groups, None, image)
        self.door_name = door_name
        self.game = game

    def update(self, player):
        self.collisions(player)

    def collisions(self, player):
        if player.rect.colliderect(self.hitbox):
            self.game.set_state(self.door_name)
            player.hitbox.topleft = (336 ,624)


