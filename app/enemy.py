import random
import pygame
class Enemy:
    def __init__(self, display):
        self.display = display
        self.screen = self.display.game.screen
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 600)
        self.w = 50
        self.h = 50
        self.update_rect()
        self.speed = 1
        self.display.objects.append(self)

    def render(self):
        self.update_rect()
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
