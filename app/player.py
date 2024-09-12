import random
import time

import pygame.draw
from app import config, game, bullet, custom_images

phase = 0
direction = 0
class Player:
    def __init__(self, display):
        self.hpHeight = 30
        self.gameWidth = int(config.read_config()['width'])
        self.gameHeight = int(config.read_config()['height'])
        self.display = display
        self.radius = 40
        self.x = (self.gameWidth - self.radius) / 2
        self.y = (self.gameHeight - self.radius) / 2
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.clicked = False
        self.velUp = 0
        self.velRight = 0
        self.maxSpeed = 6
        self.control = 0.90
        if phase == 1:
            self.control = 0.15
        self.wind = 0
        self.windStrength = 1.3
        self.confusion = False
        self.green = (30, 200, 30)
        self.money = 0
        self.windCap = self.windStrength * 6
        self.lanterns = 0
        self.lanternPrice = 20


        self.maxHp = 100
        self.hp = self.maxHp

        self.reload_start = 0
        self.start_reloading = False
        self.pistolMaxBullets = 10
        self.arMaxBullets = 30
        self.pistolShootingSpeed = 0.5
        self.pistolReloadSpeed = 3
        self.ShootingTimer = 0
        self.arShootingSpeed = 0.25
        self.arReloadSpeed = 3
        self.shotSpeedModifier = 1
        self.pistolDamage = 22
        self.arDamage = 12

        self.currentWeapon = 'pistol'
        self.currentMaxBullets = self.pistolMaxBullets
        self.bullets = self.currentMaxBullets
        self.pistolBullets = self.bullets
        self.arBullets = self.arMaxBullets
        self.currentShootingSpeed = self.pistolShootingSpeed
        self.currentReloadSpeed = self.pistolReloadSpeed
        self.currentDamage = self.pistolDamage
        self.weapons = 1
        self.weaponPrice = 1


        self.img = custom_images.Custom_image(self.display, 'img/player/player_default.png', self.x, self.y, self.radius* 2, self.radius * 2, append=False)


        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        self.display.objects.append(self)


    def render(self):
        self.movement()
        # pygame.draw.rect(self.display.screen, (255, 0, 255), self.rect)
        self.img.render()
        if self.clicked and self.currentWeapon != 'pistol':
            if self.bullets > 0 and self.start_reloading == False:
                if time.time() - self.ShootingTimer > self.currentShootingSpeed:
                    self.shoot()
                    self.ShootingTimer = time.time()
            else:
                if time.time() - self.reload_start > self.currentReloadSpeed:
                    self.reload_start = time.time()
                    self.start_reloading = True

    def events(self, event):
        #player movement capture
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.left = True
            elif event.key == pygame.K_d:
                self.right = True
            elif event.key == pygame.K_w:
                self.up = True
            elif event.key == pygame.K_s:
                self.down = True

            elif event.key == pygame.K_1 and self.money >= 30 and self.hp < self.maxHp:
                self.money -= 30
                self.hp = self.maxHp

            elif event.key == pygame.K_2 and self.money >= self.lanternPrice and self.lanterns <= 4:
                self.lanterns += 1
                self.money -= self.lanternPrice
                self.lanternPrice *= 2

            elif event.key == pygame.K_3 and self.money >= self.weaponPrice and self.weapons == 1:
                self.weapons += 1
                self.money -= self.weaponPrice
                self.weaponPrice *= 2
                self.currentWeapon = 'ar'
                self.pistolBullets = self.bullets
                self.bullets = self.arMaxBullets

            elif event.key == pygame.K_r and not self.start_reloading:
                self.start_reloading = True
                self.reload_start = time.time()


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.left = False
            elif event.key == pygame.K_d:
                self.right = False
            elif event.key == pygame.K_w:
                self.up = False
            elif event.key == pygame.K_s:
                self.down = False

        elif event.type == pygame.MOUSEWHEEL and not self.start_reloading:
            if event.y == 1:
                if self.weapons == 2 and self.currentWeapon == 'pistol':
                    self.pistolBullets = self.bullets
                    self.bullets = self.arBullets
                    self.currentWeapon = 'ar'
            elif event.y == -1:
                if self.weapons == 2 and self.currentWeapon == 'ar':
                    self.arBullets = self.bullets
                    self.bullets = self.pistolBullets
                    self.currentWeapon = 'pistol'



        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.clicked = True
            pass

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.bullets > 0 and self.start_reloading == False:
                if time.time() - self.ShootingTimer > self.currentShootingSpeed:
                    self.shoot()
                    self.ShootingTimer = time.time()
            else:
                if time.time() - self.reload_start > self.currentReloadSpeed:
                    self.reload_start = time.time()
                    self.start_reloading = True
        if self.currentWeapon == 'pistol':
            self.currentMaxBullets = self.pistolMaxBullets
            self.currentShootingSpeed = self.pistolShootingSpeed * self.shotSpeedModifier
            self.currentReloadSpeed = self.pistolReloadSpeed * self.shotSpeedModifier
            self.currentDamage = self.pistolDamage

        elif self.currentWeapon == 'ar':
            self.currentMaxBullets = self.arMaxBullets
            self.currentShootingSpeed = self.arShootingSpeed * self.shotSpeedModifier
            self.currentReloadSpeed = self.arReloadSpeed * self.shotSpeedModifier
            self.currentDamage = self.arDamage

    def shoot(self):
        if self.bullets > 0:
            self.bullets -= 1
            bullet.Bullet(self.display, self, (self.x, self.y), pygame.mouse.get_pos())

    def reload_upadate_checker(self):
        if self.start_reloading:
            if time.time() - self.reload_start > self.currentReloadSpeed:
                self.reload()
                self.start_reloading = False
    def reload(self):
        self.bullets = self.currentMaxBullets


    def movement(self):

        if self.confusion:
            self.confuse()




        if self.up and self.velUp < self.maxSpeed:
            self.velUp += self.control
        if self.velUp > 0 and not self.up:
            if self.velUp >= self.control:
                self.velUp -= self.control
            else:
                self.velUp = 0


        if self.down and self.velUp > -self.maxSpeed:
            self.velUp -= self.control
        if self.velUp < 0 and not self.down:
            if self.velUp <= -self.control:
                self.velUp += self.control
            else:
                self.velUp = 0


        if self.right and self.velRight < self.maxSpeed:
            self.velRight += self.control
        if self.velRight > 0 and not self.right:
            if self.velRight >= self.control:
                self.velRight -= self.control
            else:
                self.velRight = 0


        if self.left and self.velRight > -self.maxSpeed:
            self.velRight -= self.control
        if self.velRight < 0 and not self.left:
            if self.velRight <= -self.control:
                self.velRight += self.control
            else:
                self.velRight = 0


        if self.wind == 1:
            if self.velUp < self.maxSpeed + self.windCap:
                self.velUp += self.windStrength / 1.5
            else:
                self.velUp = self.windCap

        if self.wind == 2:
            if self.velRight < self.maxSpeed + self.windCap:
                self.velRight += self.windStrength / 1.5
            else:
                self.velRight = self.windCap

        if self.wind == 3:
            if self.velUp > -self.maxSpeed - self.windCap:
                self.velUp -= self.windStrength / 1.5
            else:
                self.velUp = -self.windCap

        if self.wind == 4:
            if self.velRight > -self.maxSpeed - self.windCap:
                self.velRight -= self.windStrength / 1.5
            else:
                self.velRight = -self.windCap


        if self.velUp < 0:
            if self.y < self.gameHeight - self.radius:
                if self.y < self.gameHeight - self.radius + self.velUp:
                    self.y -= self.velUp
                else:
                    self.y = self.gameHeight - self.radius

        else:
            if self.y > self.radius + self.hpHeight:
                if self.y > self.radius + self.velUp + self.hpHeight:
                    self.y -= self.velUp
                else:
                    self.y = self.radius + self.hpHeight

        if self.velRight < 0:
            if self.x > self.radius:
                if self.x > self.radius - self.velRight:
                    self.x += self.velRight
                else:
                    self.x = self.radius

        else:
            if self.x < self.gameWidth - self.radius:
                if self.x < self.gameWidth - self.radius - self.velRight:
                    self.x += self.velRight
                else:
                    self.x = self.gameWidth - self.radius

        if self.confusion:
            self.confuse()

        self.update_rect()
        if phase == 0:
            self.control = 1
            self.confusion = False
            self.wind = 0
            self.shotSpeedModifier = 1
        elif phase == 1:
            self.control = 0.15
        elif phase == 2:
            self.shotSpeedModifier = 2
        elif phase == 4:
            self.confusion = True
        elif phase == 5:
            self.wind = direction

        self.img.x = self.x
        self.img.y = self.y


    def confuse(self):
        right, left, up, down = False, False, False, False
        if self.left:
            right = True
        else:
           right == False
        if self.right:
            left = True
        else:
           left == False
        if self.up:
            down = True
        else:
           down == False
        if self.down:
            up = True
        else:
           up == False
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.display.fog_of_storms[self.lanterns].x = self.x
        self.display.fog_of_storms[self.lanterns].y = self.y

def getPhase(fase):
    global direction
    global phase
    phase = fase
    if phase == 5:
        direction = random.randint(1, 4)

