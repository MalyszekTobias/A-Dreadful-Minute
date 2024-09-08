import pygame.draw


class player:
    def __init__(self, display):
        self.display = display

        self.display.objects.append(self)

    def render(self):
        pygame.draw.rect(self.display.screen, (255, 255, 255), (50, 50, 100, 100))

    def events(self, event):
        pass