from random import random
import random
import pygame.time
import time
from app import custom_text, custom_images, button, player, enemy

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
        custom_text.Custom_text(self, self.game.width/2, self.game.height/3, None, 100, 'A Dreadful Minute', text_color='Green')
        button.Button(self, 'settings', self.game.width / 2 - 150, self.game.height * 0.75, 300, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.75 - 100, 300, 75, (0, 0, 0), outline_color='white', text='Start', text_color='white')


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Settings',
                                text_color='White')
        self.save_and_exit = button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white', text=' Save & exit', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['start_screen']
        else:
            for obj in self.objects:
                obj.events(event)

class settings_screen_v2(settings_screen):
    def __init__(self, game):
        settings_screen.__init__(self, game)
        self.save_and_exit.delete()
        self.save_and_exit = button.Button(self, 'pause_display', 25, self.game.height - 100, 200, 75, (0, 0, 0),
                                      outline_color='white', text=' Save & exit', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['pause_display']
        else:
            for obj in self.objects:
                obj.events(event)

class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        # if self.game.current_display == self.game.displays['game_display']:
        #     print("triggered")
        print("triggered")
        time_ = random.randint(10000, 30000)
        pygame.time.set_timer(self.game.FLASHBANG, time_)
        self.player = player.Player(self)
        self.enemies = []
        self.time = time.time()
    def mainloop(self):
        if time.time() - self.time >= 3:
            for x in range(random.randint(1, 5)):
                self.enemies.append(enemy.Enemy(self))
            self.time = time.time()
        for ene in self.enemies:
            ene.move()
    def thunder(self):
        pass

    def events(self, event):
        if event.type == self.game.FLASHBANG:
            # self.flashbang()
            print("flash")
            self.screen.fill('white')
            pygame.display.update()
            pygame.time.wait(80)

            time = random.randint(4000, 10000)
            pygame.time.set_timer(self.game.THUNDER, time)

        elif event.type == self.game.THUNDER:
            print("thunder")
            self.thunder()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['pause_display']

        else:
            for obj in self.objects:
                obj.events(event)

        if self.game.started:
            self.game.started = False
            print("triggered")
            time = random.randint(1000, 1001)
            pygame.time.set_timer(self.game.FLASHBANG, time)

class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Paused', text_color='White')
        button.Button(self, 'settings_v2', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 300, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45, 300, 75, (0, 0, 0), outline_color='white', text='Resume', text_color='white')
        button.Button(self, 'start_screen', self.game.width / 2 - 150, self.game.height * 0.45 + 200, 300, 75, (0, 0, 0), outline_color='white', text=' Exit', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['game_display']
        else:
            for obj in self.objects:
                obj.events(event)
