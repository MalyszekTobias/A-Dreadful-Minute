import random
import time

import pygame.draw
from app import config, game, bullet, custom_images

phase = 0
direction = 0
class Player:
    def __init__(self, display):
        self.hpHeight = 50
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
        self.wind = 0
        self.confusion = False
        self.green = (30, 200, 30)
        self.money = 0
        self.lanterns = 0
        self.bombs = 0
        self.maxHp = 150
        self.hp = self.maxHp
        self.reload_start = 0
        self.start_reloading = False
        self.ShootingTimer = 0
        self.shotSpeedModifier = 1
        self.easy = None


        self.recoil = 5




        self.pistolMaxBullets = 10
        self.arMaxBullets = 30
        self.miniMaxBullets = 100
        self.flameMaxBullets = 150
        self.pistolShootingSpeed = 0.4
        self.arShootingSpeed = 0.25
        self.miniShootingSpeed = 0.05
        self.flameShootingSpeed = 0.015
        self.pistolReloadSpeed = 2.2
        self.arReloadSpeed = 3.5
        self.miniReloadSpeed = 3
        self.flameReloadSpeed = 3
        self.pistolDamage = 22
        self.arDamage = 25
        self.miniDamage = 9
        self.flameDamage = 0.7
        self.pistolRecoil = 6
        self.arRecoil = 4
        self.miniRecoil = 2
        self.flameRecoil = 0



        self.currentWeapon = 'pistol'
        self.currentMaxBullets = self.pistolMaxBullets
        self.bullets = self.currentMaxBullets
        self.pistolBullets = self.bullets
        self.arBullets = self.arMaxBullets
        self.miniBullets = self.miniMaxBullets
        self.flameBullets = self.flameMaxBullets
        self.currentShootingSpeed = self.pistolShootingSpeed
        self.currentReloadSpeed = self.pistolReloadSpeed
        self.currentDamage = self.pistolDamage
        self.weapons = 1
        self.pasthp = self.hp
        self.hit = False
        self.cooldown = 0


        self.img = custom_images.Custom_image(self.display, 'img/player/player_default.png', self.x, self.y, self.radius* 2, self.radius * 2, append=False)


        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        self.display.objects.append(self)


    def render(self):
        if self.hp < self.pasthp:
            self.pasthp = self.hp
            self.cooldown = 25
        if self.hit:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.hit = False

        print(self.currentWeapon)
        self.movement()
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

    def update_diff(self):
        if self.easy:
            self.control = 1
            self.windControl = 0.20
            self.windStrength = 1.3
            self.windCap = self.windStrength * 6
            self.lanternPrice = 12
            self.weaponPrice = 40
            self.bombPrice = 20
            self.mediKits = 1
            self.mediKitPrice = 20
            self.bombs = 1
        else:
            self.control = 0.8
            self.windControl = 0.15
            self.windStrength = 1.4
            self.windCap = self.windStrength * 5
            self.lanternPrice = 16
            self.weaponPrice = 50
            self.bombPrice = 30
            self.mediKits = 0
            self.mediKitPrice = 30

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

            elif event.key == pygame.K_e and self.bombs > 0:
                bullet.Bullet(self.display, self, (self.x, self.y), pygame.mouse.get_pos(), 5, True, 0)
                self.bombs -= 1

            elif event.key == pygame.K_q and self.mediKits > 0 and self.hp < self.maxHp:
                self.hp = self.maxHp
                self.mediKits -= 1

            elif phase == 0:

                if event.key == pygame.K_1 and self.money >= 30:
                    self.money -= self.mediKitPrice
                    self.mediKits += 1

                elif event.key == pygame.K_2 and self.money >= self.lanternPrice and self.lanterns <= 4:
                    self.lanterns += 1
                    self.money -= self.lanternPrice
                    self.lanternPrice *= 2

                elif event.key == pygame.K_3 and self.money >= self.weaponPrice:
                    if self.weapons == 1:
                        self.weapons += 1
                        self.money -= self.weaponPrice
                        self.weaponPrice *= 2
                        self.currentWeapon = 'ar'
                        self.pistolBullets = self.bullets
                        self.bullets = self.arMaxBullets
                        self.recoil = self.arRecoil

                    elif self.weapons == 2:
                        self.weapons += 1
                        self.money -= self.weaponPrice
                        self.weaponPrice *= 2
                        if self.currentWeapon == 'pistol':
                            self.pistolBullets = self.bullets
                        elif self.currentWeapon == 'ar':
                            self.arBullets = self.bullets
                        self.bullets = self.miniMaxBullets
                        self.recoil = self.miniRecoil
                        self.currentWeapon = 'miniGun'

                    elif self.weapons == 3:
                        self.weapons += 1
                        self.money -= self.weaponPrice
                        self.weaponPrice *= 2
                        if self.currentWeapon == 'pistol':
                            self.pistolBullets = self.bullets
                        elif self.currentWeapon == 'ar':
                            self.arBullets = self.bullets
                        elif self.currentWeapon == 'miniGun':
                            self.miniBullets = self.bullets
                        self.bullets = self.flameBullets
                        self.recoil = self.flameRecoil
                        self.currentWeapon = 'flameThrower'


                elif event.key == pygame.K_4 and self.money >= self.bombPrice:
                    self.bombs += 1
                    self.money -= self.bombPrice

            if event.key == pygame.K_r and not self.start_reloading:
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

                elif self.weapons == 3:
                    if self.currentWeapon == 'pistol':
                        self.pistolBullets = self.bullets
                        self.bullets = self.arBullets
                        self.currentWeapon = 'ar'
                    elif self.currentWeapon == 'ar':
                        self.arBullets = self.bullets
                        self.bullets = self.miniBullets
                        self.currentWeapon = 'miniGun'

                elif self.weapons == 4:
                    if self.currentWeapon == 'pistol':
                        self.pistolBullets = self.bullets
                        self.bullets = self.arBullets
                        self.currentWeapon = 'ar'
                    elif self.currentWeapon == 'ar':
                        self.arBullets = self.bullets
                        self.bullets = self.miniBullets
                        self.currentWeapon = 'miniGun'
                    elif self.currentWeapon == 'miniGun':
                        self.miniBullets = self.bullets
                        self.bullets = self.flameBullets
                        self.currentWeapon = 'flameThrower'
            elif event.y == -1:
                if self.currentWeapon == 'ar':
                    self.arBullets = self.bullets
                    self.bullets = self.pistolBullets
                    self.currentWeapon = 'pistol'

                elif self.currentWeapon == 'miniGun':
                    self.miniBullets = self.bullets
                    self.bullets = self.arBullets
                    self.currentWeapon = 'ar'

                elif self.currentWeapon == 'flameThrower':
                    self.flameBullets = self.bullets
                    self.bullets = self.miniBullets
                    self.currentWeapon = 'miniGun'



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
            self.recoil = self.pistolRecoil

        elif self.currentWeapon == 'ar':
            self.currentMaxBullets = self.arMaxBullets
            self.currentShootingSpeed = self.arShootingSpeed * self.shotSpeedModifier
            self.currentReloadSpeed = self.arReloadSpeed * self.shotSpeedModifier
            self.currentDamage = self.arDamage
            self.recoil = self.arRecoil

        elif self.currentWeapon == 'miniGun':
            self.currentMaxBullets = self.miniMaxBullets
            self.currentShootingSpeed = self.miniShootingSpeed * self.shotSpeedModifier
            self.currentReloadSpeed = self.miniReloadSpeed * self.shotSpeedModifier
            self.currentDamage = self.miniDamage + random.randint(0, 1)
            self.recoil = self.miniRecoil

        elif self.currentWeapon == 'flameThrower':
            self.currentMaxBullets = self.flameMaxBullets
            self.currentShootingSpeed = self.flameShootingSpeed
            self.currentReloadSpeed = self.flameReloadSpeed * self.shotSpeedModifier
            self.currentDamage = self.flameDamage / self.shotSpeedModifier
            self.recoil = self.flameRecoil

    def shoot(self):
        if self.bullets > 0:
            self.bullets -= 1
            if self.currentWeapon == 'flameThrower':
                bullet.Bullet(self.display, self, (self.x, self.y), pygame.mouse.get_pos(), 22, False, 13)

            else:
                bullet.Bullet(self.display, self, (self.x, self.y), pygame.mouse.get_pos(), 5, False, 20)

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
            self.control = 0.25
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

