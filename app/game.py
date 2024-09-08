import pygame
from app import config, display, custom_text, player

class Game:
    def __init__(self):
        pygame.init()

        config.set_config()

        self.cfg = config.read_config()

        self.version = self.cfg['version']
        self.width = int(self.cfg['width'])
        self.height = int(self.cfg['height'])
        self.fps = float(self.cfg['fps'])
        self.title = self.cfg['title']
        self.enable_debug = int(self.cfg['enable_debug'])

        self.clock = pygame.time.Clock()
        self.font = None

        self.run = True

        self.objects = []

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{self.title} (v {self.version})")

        self.displays = {'template_display': display.basic_display(self), 'start_screen': display.start_screen(self), 'settings_screen': display.settings_screen(self), 'game_display': display.game_display(self)}
        self.current_display = self.displays['game_display']

        self.pointing_at = []

        self.debug = False
        self.debug_items = [custom_text.Custom_text(self, 12, 15, self.font, 30, f'Current version: {self.version}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 45, self.font, 30, f'Resolution: {self.width}x{self.height}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 75, self.font, 30, f'FPS cap: {self.fps}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 105, self.font, 30, f'FPS: {self.clock.get_fps()}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 135, self.font, 30, f'Objects in memory: {len(self.current_display.objects)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 165, self.font, 30, f'Current display: {type(self.current_display)}', text_color='white', center=False),
                            custom_text.Custom_text(self, 12, 195, self.font, 30, f'Pointing at: {self.pointing_at}', text_color='white', center=False)]


        for debug_item in self.debug_items:
            debug_item.hidden = True

        self.mainloop()

    def mainloop(self):
        while self.run:
            self.events()
            self.render()
            self.update()
            self.clock.tick(self.fps)

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
        player.Player.tickSignal()

    def render(self):
        self.screen.fill('black')
        self.current_display.render()

        for object in self.objects:
            object.render()

    def update(self):
        if self.debug:

            for obj in self.current_display.objects:
                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                    if obj not in self.pointing_at:
                        self.pointing_at.append(obj)

            i = []
            for obj in self.pointing_at:
                if obj.rect.collidepoint(pygame.mouse.get_pos()) == False:
                    i.append(obj)
            for obj in i:
                self.pointing_at.remove(obj)
            i = []


            self.debug_items[3].update_text(f'FPS: {self.clock.get_fps()}')
            self.debug_items[4].update_text(f'Objects in memory: {len(self.current_display.objects)}')
            self.debug_items[5].update_text(f'Current display: {type(self.current_display)}')
            self.debug_items[6].update_text(f'Pointing at: {self.pointing_at}')


        pygame.display.update()
        pygame.display.flip()
