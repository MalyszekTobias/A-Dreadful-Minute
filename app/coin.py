import random

import pygame.draw
from app import config, game

class Coin:
    def __init__(self, display):
        self.x = random.randint(30, 970)
        self.y = random.randint(30, 970)
        self.radius = 12
        self.display = display
        self.yellow1 = (245, 245, 51)
        self.yellow2 = (245, 190, 60)
        self.display.objects.append(self)


    def render(self):
        pygame.draw.circle(self.display.screen, self.yellow2, (self.x, self.y), self.radius)
        pygame.draw.circle(self.display.screen, self.yellow1, (self.x, self.y), self.radius - 4)

    def events(self, event):
        pass