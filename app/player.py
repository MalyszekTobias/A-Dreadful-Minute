import pygame.draw


class player:
    def __init__(self, display):
        self.display = display
        self.x = 100
        self.y = 100

        self.rect = pygame.Rect(self.x, self.y, 100, 100)

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


