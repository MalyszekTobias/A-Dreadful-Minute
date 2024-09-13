from random import random
import random

from pygame.examples.scrap_clipboard import screen

import app.game
import pygame.time
import time
from app import custom_text, custom_images, button, player, enemy, coin, game
from app.custom_images import Custom_image
import img
import math, itertools

minEnemies, maxEnemies = 3, 4


def color_cycle():
    period = 500
    t = 0
    while True:
        red = int((math.sin(t * 2 * math.pi / period) + 1) * 127.5)
        green = int((math.sin(t * 2 * math.pi / period) + 1) * 127.5)
        blue = int((math.sin((t * 2 * math.pi / period) + math.pi) + 1) * 127.5)

        yield (red, green, blue)
        t += 1

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
        self.colors_for_title_text = itertools.cycle(color_cycle())
        self.title_text = custom_text.Custom_text(self, self.game.width/2, self.game.height/3, None, 100, 'A Dreadful Minute', text_color='Green')
        button.Button(self, 'settings', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 300, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45, 300, 75, (0, 0, 0), outline_color='white', text='Start', text_color='white')
        button.Button(self, 'kill', self.game.width / 2 - 150, self.game.height * 0.45 + 200, 300, 75,
                      (0, 0, 0), outline_color='white', text='Quit', text_color='white')

    def mainloop(self):
        color = next(self.colors_for_title_text)
        self.title_text.update_color(color, None)


class settings_screen(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Settings',
                                text_color='White')
        self.save_and_exit = button.Button(self, 'start_screen', 25, self.game.height - 100, 200, 75, (0, 0, 0), outline_color='white', text=' Save & exit', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            app.game.orderPause = True
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
            app.game.orderPause = True

            self.game.current_display = self.game.displays['pause_display']
        else:
            for obj in self.objects:
                obj.events(event)

class game_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)


        # self.game.paused = False
        # self.game.unpause()
        # print("unpaused")

        # =========================================================================================================
        self.time = time.time()
        # =========================================================================================================
        print("test")

        self.player = player.Player(self)

        self.fog_of_storms = [custom_images.Custom_image(self, f'img/{x}.png', self.player.x, self.player.y, 2400, 2400, append=False, loaded=False) for x in range(0, 6)]
        self.enemies = []
        self.coins = []
        self.coin = coin.Coin(self)
        self.bullets = []
        self.time = time.time()
        self.makeCoins = 0
        self.fog = False
        # self.rect = pygame.Rect(0, 750, 150, 150)
        # self.current_weapon = 'img/handgun.png'
        self.handgun = Custom_image(self, f"img/handgun.png", 100, 915, 150, 150, append=False)
        self.ar = Custom_image(self, f"img/ar.png", 105, 915, 150, 150, append=False)
        self.bullets_left_image = custom_images.Custom_image(self, 'img/bullet_icon.png', 220, self.game.height - 55, 50, 50, append=False)
        self.bullets_left_text = custom_text.Custom_text(self,  285, self.game.height - 50, self.game.font, 50, f'X {self.player.bullets}', text_color=(255, 255, 255), append=False)
        self.reloading_text = custom_text.Custom_text(self, 115, self.game.height - 190, self.game.font, 50, f'Reloading...', text_color=(255, 255, 255), append=False)
        self.phase_info = custom_text.Custom_text(self, self.game.width - 200, self.game.height - 115, self.game.font, 35,
                                                         f'{self.game.get_event()}',
                                                         text_color=(255, 255, 255), append=False)

        self.time_left = custom_text.Custom_text(self, self.game.width - 200, self.game.height - 65,"Comic Sans", 50,
                                                         f'{self.game.timeLeft}',
                                                         text_color=(255, 255, 255), append=False, system=True)
        self.money = custom_text.Custom_text(self, 285, self.game.height - 115, self.game.font,
                                             50, f"X {self.player.money}",
                                             text_color=(255, 255, 0), append=False, system=True)
        self.money_image = custom_images.Custom_image(self, 'img/zlotowka.png', 220, self.game.height - 115, 50, 50, append=False)


        self.bulbs = custom_text.Custom_text(self, 425, self.game.height - 115, self.game.font,
                                             50, f"X {self.player.lanterns}",
                                             text_color=(0, 0, 255), append=False, system=True)
        self.bulbs_image = custom_images.Custom_image(self, 'img/bulb.png', 370, self.game.height - 115, 50, 50,
                                                      append=False)
        # self.enemies.append(enemy.Enemy(self))
    def mainloop(self):
        global minEnemies
        global maxEnemies
        self.player.img.rotate_toward_mouse(pygame.mouse.get_pos())
        # if self.player.bullets == 0 and time.time() - self.player.reload_start > self.player.reloadSpeed:
        #     self.player.start_reloading = True
        #     self.player.reload_start = time.time()
        self.player.reload_upadate_checker()

        if time.time() - self.time >= 3:
            if self.game.phase == 0:
                for x in range(random.randint(1, 1)):
                    self.enemies.append(enemy.Enemy(self))
            else:
                for x in range(random.randint(minEnemies, maxEnemies)):
                    self.enemies.append(enemy.Enemy(self))
            self.time = time.time()

        for ene in self.enemies:
            ene.move()
        if self.makeCoins > 0:
            for i in range(self.makeCoins):
                self.coins.append(coin.Coin(self))
            self.makeCoins = 0


        for bullet in self.bullets:
            bullet.move()

        self.bullets_left_text.update_text(f'X {self.player.bullets}')
        self.phase_info.update_text(f'{self.game.get_event()}')
        self.time_left.update_text(f'{self.game.timeLeft}')
        self.money.update_text(f"X {self.player.money}")
        self.bulbs.update_text(f"X {self.player.lanterns}")
    def thunder(self):
        # pygame.mixer.Sound.play(self.game.thunder_sound)
        pygame.mixer.Channel(4).play(pygame.mixer.Sound(self.game.thunder_sound))
        # pygame.mixer.music.stop()


    def flashbang(self):
        print("flash")
        self.screen.fill('white')
        pygame.display.update()
        pygame.time.wait(80)
        self.game.make_thunder = True
    def events(self, event):
        # if event.type == self.game.FLASHBANG:
        #     # self.flashbang()
        #
        #
        #     time_temp = random.randint(4000, 10000)
        #     pygame.time.set_timer(self.game.THUNDER, time_temp)

        # elif event.type == self.game.THUNDER:
        #     print("thunder")
        #     self.thunder()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            app.game.orderPause = True

            self.game.ready = True
            self.game.current_display = self.game.displays['pause_display']

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.fog = not self.fog
        else:
            for obj in self.objects:
                obj.events(event)

    def render(self):
        for obj in self.objects:
            obj.render()
        # pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
        if self.fog:
            if self.fog_of_storms[self.player.lanterns].loaded != True:
                self.fog_of_storms[self.player.lanterns].load()
                self.fog_of_storms[self.player.lanterns].loaded = True
            self.fog_of_storms[self.player.lanterns].update_rect()
            self.fog_of_storms[self.player.lanterns].render()

        pygame.draw.rect(self.game.screen, (26, 26, 26), (20, 840, self.game.width - 40, 140), border_radius=5)
        pygame.draw.rect(self.game.screen, (40, 40, 40), (30, 850, 150, 120), border_radius=5)
        self.phase_info.render()
        self.time_left.render()
        self.bullets_left_text.render()
        self.bullets_left_image.render()
        self.money.render()
        self.money_image.render()
        self.bulbs.render()
        self.bulbs_image.render()
        if self.player.currentWeapon == 'pistol':
            self.handgun.render()
        elif self.player.currentWeapon == 'ar':
            self.ar.render()
        if self.player.start_reloading:
            self.reloading_text.render()
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (0, 0, (self.game.width * self.player.hp / self.player.maxHp), self.player.hpHeight))





class pause_display(basic_display):
    def __init__(self, game):
        basic_display.__init__(self, game)
        # self.game.paused = True
        # self.game.pause()
        # print("pause")

        custom_text.Custom_text(self, self.game.width / 2, self.game.height / 3, None, 100, 'Paused', text_color='White')
        button.Button(self, 'settings_v2', self.game.width / 2 - 150, self.game.height * 0.45 + 100, 300, 75, (0, 0, 0), outline_color='white', text='Settings', text_color='white')
        button.Button(self, 'game_display', self.game.width / 2 - 150, self.game.height * 0.45, 300, 75, (0, 0, 0), outline_color='white', text='Resume', text_color='white')
        button.Button(self, 'start_screen', self.game.width / 2 - 150, self.game.height * 0.45 + 200, 300, 75, (0, 0, 0), outline_color='white', text=' Exit', text_color='white')

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.current_display = self.game.displays['game_display']
            app.game.orderUnpause = True
            self.game.ready_u = True
        else:
            for obj in self.objects:
                obj.events(event)
