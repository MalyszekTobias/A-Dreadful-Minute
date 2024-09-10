from random import random
import random

import app.game
import pygame.time
import time
from app import custom_text, custom_images, button, player, enemy, coin, game
from app.custom_images import Custom_image


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


        self.player = player.Player(self)
        self.fog_of_storm = custom_images.Custom_image(self, 'img/fog_of_storm.png', self.player.x, self.player.y, 2000,
                                                       2000, append=False)
        self.enemies = []
        self.coins = []
        self.coin = coin.Coin(self)
        self.bullets = []
        self.time = time.time()
        self.makeCoins = 0
        self.fog = False
        # self.rect = pygame.Rect(0, 750, 150, 150)
        self.handgun = Custom_image(self, "img/handgun.png", 100, 915, 150, 150, append=False)
        self.bullets_left_image = custom_images.Custom_image(self, 'img/bullet_icon.png', 220, self.game.height - 55, 75, 75, append=False)
        self.bullets_left_text = custom_text.Custom_text(self,  290, self.game.height - 55, self.game.font, 50, f'X {self.player.bullets}', text_color=(255, 255, 255), append=False)
        self.reloading_text = custom_text.Custom_text(self, 110, self.game.height - 190, self.game.font, 50, f'Reloading...', text_color=(255, 255, 255), append=False)
        self.phase_info = custom_text.Custom_text(self, 840, 50, self.game.font, 35,
                                                         f'{self.game.get_event()}',
                                                         text_color=(255, 255, 255), append=False)
        self.time_left = custom_text.Custom_text(self, 840, 100,"Comic Sans", 50,
                                                         f'{self.game.timeLeft}',
                                                         text_color=(255, 255, 255), append=False, system=True)
        # self.enemies.append(enemy.Enemy(self))
    def mainloop(self):

        self.player.img.rotate_toward_mouse(pygame.mouse.get_pos())
        self.player.reload_upadate_checker()
        if time.time() - self.time >= 3:
            for x in range(random.randint(3, 4)):
                self.enemies.append(enemy.Enemy(self))
            self.time = time.time()

        for ene in self.enemies:
            ene.move()
        if self.makeCoins > 0:
            print(123456789)
            for i in range(self.makeCoins):
                self.coins.append(coin.Coin(self))
            self.makeCoins = 0


        for bullet in self.bullets:
            bullet.move()

        self.bullets_left_text.update_text(f'X {self.player.bullets}')
        self.phase_info.update_text(f'{self.game.get_event()}')
        self.time_left.update_text(f'{self.game.timeLeft}')
    def thunder(self):
        pygame.mixer.Sound.play(self.game.thunder_sound)
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
            self.fog_of_storm.update_rect()
            self.fog_of_storm.render()
        self.phase_info.render()
        self.time_left.render()
        self.bullets_left_text.render()
        self.bullets_left_image.render()
        pygame.draw.rect(self.game.screen, (16, 16, 16), (10, 830, 180, 160), border_radius=5)
        pygame.draw.rect(self.game.screen, (26, 26, 26), (20, 840, 160, 140), border_radius=5)
        self.handgun.render()
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
