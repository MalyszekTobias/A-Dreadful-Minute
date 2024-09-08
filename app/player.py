import pygame.draw
from app import config, game

class Player:
    def __init__(self, display):
        self.gameWidth = int(config.read_config()['width'])
        self.gameHeight = int(config.read_config()['height'])
        self.display = display
        self.radius = 25

        self.x = (self.gameWidth - self.radius) / 2
        self.y = (self.gameHeight - self.radius) / 2
        print(self.x, self.y)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.velUp = 0
        self.velRight = 0
        self.maxSpeed = 6
        self.control = 0.9
        self.wind = 0

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        self.display.objects.append(self)

    def render(self):
        self.movement()
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



    def movement(self):
        if self.up and self.velUp < self.maxSpeed:
            self.velUp += self.control
        if self.velUp > 0 and not self.up:
            if self.velUp >= self.control:
                self.velUp -= self.control
            else:
                self.velUp = 0


        if self.down and self.velUp > -self.maxSpeed:
            self.velUp -= self.control
        if self.velUp < 0 and not self.down:
            if self.velUp <= -self.control:
                self.velUp += self.control
            else:
                self.velUp = 0


        if self.right and self.velRight < self.maxSpeed:
            self.velRight += self.control
        if self.velRight > 0 and not self.right:
            if self.velRight >= self.control:
                self.velRight -= self.control
            else:
                self.velRight = 0


        if self.left and self.velRight > -self.maxSpeed:
            self.velRight -= self.control
        if self.velRight < 0 and not self.left:
            if self.velRight <= -self.control:
                self.velRight += self.control
            else:
                self.velRight = 0


        if self.velUp < 0:
            if self.y < self.gameHeight - self.radius:
                if self.y < self.gameHeight - self.radius + self.velUp:
                    self.y -= self.velUp
                else:
                    self.y = self.gameHeight - self.radius

        else:
            if self.y > self.radius:
                if self.y > self.radius + self.velUp:
                    self.y -= self.velUp
                else:
                    self.y = self.radius

        if self.velRight < 0:
            if self.x > self.radius:
                if self.x > self.radius - self.velRight:
                    self.x += self.velRight
                else:
                    self.x = self.radius

        else:
            if self.x < self.gameWidth - self.radius:
                if self.x < self.gameWidth - self.radius - self.velRight:
                    self.x += self.velRight
                else:
                    self.x = self.gameWidth - self.radius
        print(self.y)

        self.update_rect()


    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)


