from random import random
import random
import pygame.time

from app import custom_text, custom_images, button, player

class basic_display():
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.objects = []

    def render(self):
        for obj in self.objects:
            obj.render()

    def events(self, event):
        for obj in self.objects:
            obj.events(event)


class start_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width/2, self.game.height/3, None, 100, 'Drzem Game!', text_color='Green')
        button.Button(self, 'settings', self.game.width/2 - 100, self.game.height * 0.75, 200, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width/2 - 100, self.game.height * 0.75 - 100, 200, 75, (0, 0, 0), outline_color='white', text='Start', text_color='white')


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white', text=' Save & exit', text_color='white')


class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        # game.started = True
        if game.started:
            game.trigger()
        self.player = player.Player(self)
    def flashbang(self):
        self.screen.fill('white')
        self.screen.fill('black')
    def thunder(self):
        pass