import pygame.draw
from app import config, game

class Player:
    def __init__(self, display):
        self.gameWidth = int(config.read_config()['width'])
        self.gameHeight = int(config.read_config()['height'])
        self.display = display
        self.radius = 50

        self.x = (self.gameWidth - self.radius) / 2
        self.y = (self.gameHeight - self.radius) / 2
        print(self.x, self.y)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.velUp = 0
        self.velRight = 0
        self.maxSpeed = 15
        self.control = 2
        self.wind = 0

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        self.display.objects.append(self)

    def render(self):
        pygame.draw.rect(self.display.screen, (255, 0, 255), self.rect)

    def events(self, event):
        #player movement capture
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.left = True
            elif event.key == pygame.K_d:
                self.right = True
            elif event.key == pygame.K_w:
                self.up = True
            elif event.key == pygame.K_s:
                self.down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.left = False
            elif event.key == pygame.K_d:
                self.right = False
            elif event.key == pygame.K_w:
                self.up = False
            elif event.key == pygame.K_s:
                self.down = False




        self.update_rect()

    def tickSignal(self):
        self.calculateMovement()

    def calculateMovement(self):
        print(self.x)


    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)


