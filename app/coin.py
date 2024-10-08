import random
import math as Kutt
import pygame.draw
from app import config, game, custom_images
clearOrder = False

class Coin:
    def __init__(self, display):
        self.x = random.randint(30, 970)
        self.y = random.randint(70, 970)
        self.radius = 12
        self.display = display
        self.display.objects.append(self)

        self.img = custom_images.Custom_image(self.display, 'img/zlotowka.png', self.x, self.y, self.radius*2, self.radius*2)

        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


    def render(self):
        self.img.update_rect()
        self.img.render()
        if Kutt.sqrt((self.x - self.display.player.x) ** 2 + (self.y - self.display.player.y) ** 2) < self.radius + self.display.player.radius:
            self.display.player.money += 1
            self.delete()
        if clearOrder:
            self.display.player.money += random.randint(0, 1)
            self.delete()




    def events(self, event):
        pass

    def delete(self):
        self.img.delete()
        try:
            self.display.objects.remove(self)
        except:
            print("already removed")
        del self


