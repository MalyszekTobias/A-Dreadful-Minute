import pygame
from app import custom_text

class Button:  # A button class
    def __init__(self, display, action, x, y, width, height, color, text=None):  # Getting all the parameters of the button

        self.action = action

        self.display = display

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Creating a rect object

        self.display.objects.append(self)  # Adding self to objects of the screen

        if text != None:  # if there is text it's put on the button
            self.text = custom_text.Custom_text(self.display, self.x + self.width // 2, self.y + self.height // 2, None,
                                    self.height // 2, text)

    def render(self):  # Rendering a button on screen
        pygame.draw.rect(self.display.screen, self.color, self.rect, border_radius=10)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            print('clicked')

    def delete(self):
        self.display.objects.remove(self)
        del self

        self.display.objects.remove(self.text)
        del self.text
