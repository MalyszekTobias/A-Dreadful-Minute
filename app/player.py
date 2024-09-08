import pygame.draw
from app import config

class player:
    def __init__(self, display):
        self.gameWidth = int(config.read_config()['width'])
        self.gameHeight = int(config.read_config()['height'])
        self.display = display
        self.width = 100
        self.height = 100

        self.x = (self.gameWidth - self.width) / 2
        self.y = (self.gameHeight - self.height) / 2
        print(self.x, self.y)
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.display.objects.append(self)

    def render(self):
        pygame.draw.rect(self.display.screen, (255, 0, 255), self.rect)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.x -= 5

            self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, 100, 100)


