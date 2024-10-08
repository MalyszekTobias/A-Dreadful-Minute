import random
from itertools import count
from app import custom_images

import app.game
import pygame
import math as ma
from app import game
class Enemy:
    def __init__(self, display):
        self.display = display
        self.screen = self.display.game.screen
        if random.randint(0, 1):
            self.x = -30
        else:
            self.x = self.display.game.width + 30

        self.y = random.randint(50, 950)
        self.radius = 25
        # self.w = 50
        # self.h = 50
        self.update_rect()
        self.speed = 2
        self.killCount = 0
        self.damage = 10
        self.countdown = 0

        self.img = custom_images.Custom_image(self.display, 'img/enemy/enemy_default.png', self.x, self.y, self.radius*2, self.radius*2, append=False)

        self.hp = 20
        self.display.objects.append(self)

    def render(self):
        self.update_rect()
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        self.img.render()
        self.countdown -= 1


    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def move(self):
        if self.hp <= 0:
            self.delete()
        else:
            # if self.x < self.display.player.x - self.display.player.radius:
            #     self.x += self.speed
            # elif self.x > self.display.player.x - self.display.player.radius:
            #     self.x -= self.speed
            #
            # if self.y < self.display.player.y - self.display.player.radius:           # Stary kod
            #     self.y += self.speed
            # elif self.y > self.display.player.y - self.display.player.radius:
            #     self.y -= self.speed

            if self.display.player.x > self.x:
                self.x += self.get_x()
                self.y += self.get_y()
            elif self.display.player.x <= self.x:
                self.x -= self.get_x()
                self.y -= self.get_y()
            if ma.sqrt((self.x - self.display.player.x) ** 2 + (self.y - self.display.player.y) ** 2) < self.radius + self.display.player.radius:
                if self.countdown <= 0 and not self.display.player.hit:
                    self.display.player.hp -= self.damage
                    self.countdown = 75
                    self.display.player.hit = True

            # self.update_rect()
            self.img.x = self.x
            self.img.y = self.y
            self.img.update_rect()

    def events(self, event):
        pass

    def delete(self):
        self.display.objects.remove(self)
        self.display.enemies.remove(self)
        app.game.killCount += 1
        del self

    def count_a(self):
        try:
            return (self.display.player.y - self.y) / (self.display.player.x - self.x)
        except:
            return 0
    def count_angle(self):
        return ma.atan(self.count_a())
    def get_x(self):
        return ma.cos(self.count_angle())
    def get_y(self):
        return ma.sin(self.count_angle())
