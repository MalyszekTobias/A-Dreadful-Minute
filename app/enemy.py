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
        self.speed = 2
        self.killCount = 0

        self.hp = 20
        self.display.objects.append(self)

    def render(self):
        self.update_rect()
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self):
        if self.hp <= 0:
            self.delete()
        else:
            if self.x < self.display.player.x:
                self.x += self.speed
            elif self.x > self.display.player.x:
                self.x -= self.speed

            if self.y < self.display.player.y:
                self.y += self.speed
            elif self.y > self.display.player.y:
                self.y -= self.speed

            self.update_rect()

    def events(self, event):
        pass

    def delete(self):
        self.display.objects.remove(self)
        self.display.enemies.remove(self)
        self.killCount += 1
        del self
