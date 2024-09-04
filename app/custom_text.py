import pygame

class Custom_text:  # A class that generates text
    def __init__(self, display, x, y, font, font_height, text, text_color='Black', background_color=None, center=True):

        self.display = display

        self.x = x
        self.y = y
        self.font_height = font_height
        self.text = text
        self.text_color = text_color
        self.background_color = background_color

        self.hidden = False

        self.center = center

        self.font = pygame.font.Font(font, self.font_height)

        self.text_to_render = self.font.render(self.text, True, self.text_color, self.background_color)
        self.text_rect = self.text_to_render.get_rect()

        if self.center:  # If self.center == True it sets the center of the text as self.x and self.y
            self.text_rect.center = (self.x, self.y)
        else:  # Else it set self.x and self.y as the top left corner of the text
            self.text_rect.center = (self.x + self.text_rect.width//2, self.y + self.text_rect.height//2)

        self.display.objects.append(self)

    def render(self):  # Renders the text
        if not self.hidden:
            self.display.screen.blit(self.text_to_render, self.text_rect)

    def events(self, event):  # For now just passes when checking events
        pass

    def delete(self):
        self.display.objects.remove(self)
        del self

    def update_text(self, text):
        self.text = text
        self.text_to_render = self.font.render(self.text, True, self.text_color, self.background_color)
        self.text_rect = self.text_to_render.get_rect()

        if self.center:  # If self.center == True it sets the center of the text as self.x and self.y
            self.text_rect.center = (self.x, self.y)
        else:  # Else it set self.x and self.y as the top left corner of the text
            self.text_rect.center = (self.x + self.text_rect.width // 2, self.y + self.text_rect.height // 2)