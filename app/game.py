import random
import time

import app.coin
import pygame
from app import config, display, custom_text, player
from sounds import *
from app import custom_images


orderPause = True
orderUnpause = False
killCount = 0


class Game:
    def __init__(self):
        pygame.init()

        config.set_config()

        self.cfg = config.read_config()

        # self.FLASHBANG = pygame.USEREVENT + 1
        # self.THUNDER = pygame.USEREVENT + 2
        self.make_thunder = False
        self.version = self.cfg['version']
        self.width = int(self.cfg['width'])
        self.height = int(self.cfg['height'])
        self.fps = float(self.cfg['fps'])
        self.title = self.cfg['title']
        self.fullscreen = int(self.cfg['full-screen'])
        self.thunder_sound = pygame.mixer.Sound("sounds/thunder.ogg")
        self.bang = pygame.mixer.Sound("sounds/bang.ogg")
        # pygame.mixer.Channel(0).load('sounds/light-rain-109591.wav')
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/light-rain-109591.ogg'))
        self.enable_debug = int(self.cfg['enable_debug'])
        self.started = False
        self.clock = pygame.time.Clock()
        self.font = None
        self.start_time = 0
        self.start_time_flash = 0
        self.start_time_thunder = 0
        self.time_flash = 0
        self.time_thunder = 0
        self.paused = False
        self.paused_flash = 0
        self.paused_thunder = 0
        self.pauseTotal = 0
        self.LastShot = 1
        self.pauseStart = None
        self.currentPauseTime = 0
        self.isPaused = True
        self.ready = True
        self.ready_u = False
        self.calmTime = 15
        self.stormTime = 45
        self.totalKills = 0
        self.trueTime = 0
        self.timeLeft = 5
        self.phase = 0
        self.roundCounter = 0

        self.run = True
        killCount = 0
        pygame.mouse.set_visible(False)


        self.objects = []
        self.background = pygame.image.load('img/background.png')
        self.screen = pygame.display.set_mode((self.width, self.height))
        if self.fullscreen:
            pygame.display.toggle_fullscreen()
        pygame.display.set_caption(f"{self.title} (v {self.version})")

        self.displays = {'template_display': display.basic_display(self), 'start_screen': display.start_screen(self), 'game_display': display.game_display(self), 'pause_display': display.pause_display(self)}
        self.current_display = self.displays['start_screen']

        self.pointing_at = []
        self.phase = 0
        self.phases = [1, 2, 3, 4, 5]
        self.startTime = round(time.time())

        self.debug = False
        self.debug_items = [custom_text.Custom_text(self, 12, 15, self.font, 30, f'Current version: {self.version}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 45, self.font, 30, f'Resolution: {self.width}x{self.height}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 75, self.font, 30, f'FPS cap: {self.fps}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 105, self.font, 30, f'FPS: {self.clock.get_fps()}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 135, self.font, 30, f'Objects in memory: {len(self.current_display.objects)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 165, self.font, 30, f'Current display: {type(self.current_display)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 195, self.font, 30, f'Pointing at: {self.pointing_at}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 225, self.font, 30, f'Phase: {self.phase}', text_color='white', center=False)]
        self.crosshair = custom_images.Custom_image(self.current_display, 'img/crosshair.png', pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 25, 25, append=False)


        for debug_item in self.debug_items:
            debug_item.hidden = True
        self.mainloop()

    def check_pause(self):
        if self.isPaused and self.ready:
            self.ready = False
            self.ready_u = True
            self.pause()

    def check_unpause(self):
        if not self.isPaused and self.ready_u:
            self.ready_u = False
            self.ready = True
            self.unpause()

    # def end(self):
    #     if ended:
    def pause(self):
        # pygame.mixer.music.pause()
        self.paused_flash = pygame.time.get_ticks() - self.start_time_flash
        self.paused_thunder = pygame.time.get_ticks() - self.start_time_thunder

    def unpause(self):
        # pygame.mixer.music.unpause()
        self.start_time_flash = pygame.time.get_ticks()
        self.start_time_thunder = pygame.time.get_ticks()
        if self.time_flash == 0:
            self.time_flash = 0
        else:
            self.time_flash -= self.paused_flash
        self.time_thunder -= self.paused_thunder
        self.paused = False

    def mainloop(self):
        killCount = 0
        while self.run:

            self.phaseCheck()
            if self.current_display == self.displays['game_display'] or self.current_display == self.displays['start_screen']:
                self.current_display.mainloop()
            if orderPause:
                self.pausePhase()
            if orderUnpause:
                self.unpausePhase()
            if self.isPaused:
                self.currentPauseTime = round(time.time()) - self.pauseStart



            self.events()
            self.render()
            self.update()
            self.clock.tick(self.fps)
            # self.thunderstorm()
            self.check_pause()
            self.check_unpause()
            # self.end()

            if not self.isPaused:
                if self.started:
                    self.started = False
                    self.start_time_flash = pygame.time.get_ticks()
                    self.time_flash = random.randint(10000, 15000)  # You can edit time
                    # print("start time: ", self.start_time_flash)
                    # print("time temp: ", self.time_flash)
                    check = True
                try:
                    if pygame.time.get_ticks() - self.start_time_flash >= self.time_flash and check == True and self.current_display == \
                            self.displays['game_display']:
                        check = False
                        # print("triggered")
                        self.current_display.flashbang()
                except:
                    pass

                # Thunders
                if self.make_thunder:
                    self.make_thunder = False
                    self.start_time_thunder = pygame.time.get_ticks()
                    self.time_thunder = random.randint(1000, 4000)  # You can edit time
                    # print("start time: ", self.start_time_thunder)
                    # print("time thunder: ", self.time_thunder)
                    check_thunder = True
                try:
                    if pygame.time.get_ticks() - self.start_time_thunder >= self.time_thunder and check_thunder == True and self.current_display == \
                            self.displays['game_display']:
                        check_thunder = False
                        # print("triggered")
                        self.current_display.thunder()
                except:
                    pass
                # if self.make_thunder:
                #     self.make_thunder = False
                #     self.start_time_thunder = pygame.time.get_ticks()
                #     self.time_thunder = random.randint(1000, 5000)  # You can edit time
                #     # print("start time: ", self.start_time_thunder)
                #     # print("time thunder: ", self.time_thunder)
                #     check_thunder = True
                # try:
                #     if pygame.time.get_ticks() - self.start_time_thunder >= self.time_thunder and check_thunder == True and self.current_display == \
                #             self.displays['game_display']:
                #         check_thunder = False
                #         # print("triggered")
                #         self.current_display.thunder()
                # except:
                #     pass




    def pausePhase(self):
        global orderPause
        orderPause = False
        self.isPaused = True
        self.pauseStart = round(time.time())



    def unpausePhase(self):
        global orderUnpause
        orderUnpause = False
        self.isPaused = False
        self.pauseTotal += self.currentPauseTime
        self.currentPauseTime = 0


    def phaseCheck(self):
        if self.findPhase() == 'storm start':
            self.started = True
            app.coin.clearOrder = True
            try:
                self.phase = random.choice(self.phases)
                self.phases.remove(self.phase)
                player.getPhase(self.phase)
                print('storm starts: ', self.phase)
            except:
                self.phases = [1, 2, 3, 4, 5]
        elif self.findPhase() == 'storm end':
            app.coin.clearOrder = False
            self.phase = 0
            global killCount
            self.totalKills += killCount
            if self.current_display == self.displays['game_display']:
                self.current_display.makeCoins = killCount
            killCount = 0
            self.roundCounter += 1
            if self.roundCounter % 2 == 0:
                display.minEnemies += 1
            else:
                display.maxEnemies += 1


            print('storm ends')
            player.getPhase(self.phase)


    def findPhase(self):
        trueTime = round(time.time()) - self.startTime - self.currentPauseTime - self.pauseTotal
        self.trueTime = trueTime
        trueTimeArchive = trueTime
        nextDecrease = self.calmTime
        while trueTime > nextDecrease:
            trueTime -= nextDecrease
            if nextDecrease == self.calmTime:
                nextDecrease = self.stormTime
            else:
                nextDecrease = self.calmTime
        if self.phase == 0:
            self.timeLeft = self.calmTime - trueTime

            if trueTimeArchive % (self.calmTime + self.stormTime) == 0:
                self.timeLeft = self.calmTime
            if trueTime == self.calmTime:
                return 'storm start'
        else:
            self.timeLeft = self.stormTime - trueTime
            if trueTime == self.calmTime:
                self.timeLeft = self.stormTime
                if (trueTimeArchive - 5) % (self.stormTime + self.calmTime) != 0:
                    self.timeLeft = self.stormTime - trueTime
            if trueTime == self.stormTime:
                return 'storm end'

    def get_event(self):
        if self.phase == 0:
            return "Time left before the storm:"
        else:
            return "Storm time left:"

    # def trigger(self):
    #     print('triggered')
    #     time = random.randint(15000, 30000)
    #     pygame.time.set_timer(self.FLASHBANG, time)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH and self.enable_debug:
                self.debug = not self.debug
                for di in self.debug_items:
                    di.hidden = not di.hidden
            else:
                self.current_display.events(event)

    def render(self):
        if self.current_display == self.displays['game_display']:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill('black')
        # self.screen.blit(self.background, (0, 0))
        self.current_display.render()

        for object in self.objects:
            object.render()

        self.crosshair.x, self.crosshair.y = pygame.mouse.get_pos()
        self.crosshair.update_rect()
        self.crosshair.render()

    def update(self):
        if self.debug:

            for obj in self.current_display.objects:
                try:
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        if obj not in self.pointing_at:
                            self.pointing_at.append(obj)
                except:
                    pass
            i = []
            for obj in self.pointing_at:
                if obj.rect.collidepoint(pygame.mouse.get_pos()) == False or obj.display != self.current_display:
                    i.append(obj)
            for obj in i:
                self.pointing_at.remove(obj)
            i = []


            self.debug_items[3].update_text(f'FPS: {self.clock.get_fps()}')
            self.debug_items[4].update_text(f'Objects in memory: {len(self.current_display.objects)}')
            self.debug_items[5].update_text(f'Current display: {type(self.current_display)}')
            self.debug_items[6].update_text(f'Pointing at: {self.pointing_at}')
            self.debug_items[7].update_text(f'Phase: {self.phase}')


        pygame.display.update()
        pygame.display.flip()
