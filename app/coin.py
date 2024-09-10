import random
import math as Kutt
import pygame.draw
from app import config, game

class Coin:
    def __init__(self, display):
        self.x = random.randint(30, 970)
        self.y = random.randint(50, 970)
        self.radius = 12
        self.display = display
        self.yellow1 = (245, 245, 51)
        self.yellow2 = (245, 190, 60)
        self.display.objects.append(self)


    def render(self):
        pygame.draw.circle(self.display.screen, self.yellow2, (self.x, self.y), self.radius)
        pygame.draw.circle(self.display.screen, self.yellow1, (self.x, self.y), self.radius - 4)
        if Kutt.sqrt((self.x - self.display.player.x) ** 2 + (self.y - self.display.player.y) ** 2) < self.radius + self.display.player.radius:
            self.display.player.money += 1
            self.delete()


    def events(self, event):
        pass

    def delete(self):
        self.display.objects.remove(self)
        del self
