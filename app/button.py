import app.game
import pygame
from app import custom_text

class Button:  # A button class
    def __init__(self, display, action, x, y, width, height, color, text=None, text_color='black', outline_color=None, outline_width=5):  # Getting all the parameters of the button

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
            self.text = custom_text.Custom_text(self.display, self.x + self.width / 2, self.y + self.height / 2, None,
                                    self.height // 2, text, text_color=text_color)

        self.outline_color = outline_color
        self.outline_width = outline_width

    def render(self):  # Rendering a button on screen
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.display.screen, self.get_hover_color(), self.rect, border_radius=10)
        else:
            pygame.draw.rect(self.display.screen, self.color, self.rect, border_radius=10)


        if self.outline_color != None:
            pygame.draw.rect(self.display.screen, self.outline_color, self.rect, self.outline_width, border_radius=10)

    def events(self, event):  # Checks events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):  # Checks if the button has been pressed
            if self.action == 'settings':
                app.game.isPaused = True
                self.display.game.current_display = self.display.game.displays['settings_screen']
            elif self.action == 'settings_v2':
                app.game.isPaused = True
                self.display.game.current_display = self.display.game.displays['settings_screen_v2']
            elif self.action == 'start_screen':
                app.game.isPaused = True
                self.display.game.current_display = self.display.game.displays['start_screen']
            elif self.action == 'game_display':
                app.game.isPaused = False
                print("unpause")
                self.display.game.current_display = self.display.game.displays['game_display']
            elif self.action == 'pause_display':
                app.game.isPaused = True
                print("pause")
                self.display.game.current_display = self.display.game.displays['pause_display']
            else:
                print('No action assigned to this button')

    def delete(self):
        self.display.objects.remove(self.text)
        del self.text

        self.display.objects.remove(self)
        del self

    def get_hover_color(self):
        biggest = max(self.color)
        if biggest <= 225:
            return tuple(color + 30 for color in self.color)
        else:
            return tuple(color - 30 if color >= 30 else 0 for color in self.color)
