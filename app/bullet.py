import pygame.draw
import math as Charles


class Bullet:
    def __init__(self, display, shooter, pos, mousepos, radius, boom, speed):
        self.display = display
        self.shooter = shooter
        self.x_1 = pos[0]
        self.y_1 = pos[1]
        self.boom = boom
        self.display.game.LastShot += 1
        if self.display.game.LastShot >= 4:
            self.display.game.LastShot = 1
        if not self.display.player.currentWeapon == "flameThrower":
            pygame.mixer.Channel(self.display.game.LastShot).play(self.display.game.bang)
        self.x_2 = mousepos[0]
        self.y_2 = mousepos[1]

        self.x, self.y = pos
        self.recoil = True

        self.calculate_linear_function()
        self.get_ratio()

        self.radius = radius
        self.lifetime = 21


        self.damage = 12
        self.speed = speed
        self.color = (245, 245, 51)
        if self.boom or self.radius > 5:
            self.color = (245, 145, 51)
            self.recoil = False


        self.update_rect()

        if self.a < 0:
            self.speed *= -1


        self.display.objects.append(self)
        self.display.bullets.append(self)

    def delete(self):
        self.display.objects.remove(self)
        self.display.bullets.remove(self)

        del self

    def render(self):
        # pygame.draw.line(self.display.game.screen, (255, 255, 255), (self.x_1, self.y_1), (self.x_2, self.y_2))
        pygame.draw.circle(self.display.game.screen, self.color, (self.x, self.y), self.radius)
        if self.radius > 5:
            self.lifetime -= 1
        if self.lifetime < 0:
            try:
                self.delete()
            except:
                print("already deleted")

        if self.boom and self.radius < 230:
            self.radius += 15
        elif self.boom and self.radius >= 230:
            self.delete()

    def move(self):
        if self.out_of_bounds():
            self.delete()
        else:
            self.x = ((self.ratio_x * self.speed)/self.denominator) + self.x_1
            self.y = ((self.ratio_y * self.speed)/self.denominator) + self.y_1

            self.x_1 = self.x
            self.y_1 = self.y

            if self.recoil:
                if (self.x_2 < self.shooter.x and self.y_2 > self.shooter.y) or (
                        self.x_2 > self.shooter.x and self.y_2 < self.shooter.y):
                    self.shooter.velRight = ((self.ratio_x * self.shooter.recoil) / self.denominator)
                    self.shooter.velUp = -((self.ratio_y * self.shooter.recoil) / self.denominator)
                else:

                    self.shooter.velRight = -((self.ratio_x * self.shooter.recoil) / self.denominator)
                    self.shooter.velUp = ((self.ratio_y * self.shooter.recoil) / self.denominator)

                self.shooter.update_rect()
                self.recoil = False

        self.update_rect()
        for enemy in self.display.enemies:
            if Charles.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) < self.radius + enemy.radius:
            # if enemy.rect.colliderect(self.rect):
                enemy.hp -= self.shooter.currentDamage
                if self.radius == 5:
                    try:
                        self.delete()
                    except:
                        print("already deleted")
            # self.update_rect()

    def collideCheck(self):
        for enemy in self.display.enemies:
            if Charles.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) < self.radius + enemy.radius:
                enemy.hp = 0

    def events(self, event):
        pass

    def calculate_linear_function(self):
        if self.x_1 != self.x_2:
            self.a = (self.y_2 - self.y_1)/(self.x_2 - self.x_1)
        else:
            self.a = 0
        self.b = self.y_1 - (self.a * self.x_1)

    def get_ratio(self):
        if (self.x_2 < self.shooter.x and self.y_2 > self.shooter.y) or (self.x_2 > self.shooter.x and self.y_2 < self.shooter.y):
            self.ratio_x = self.x_1 - self.x_2
            self.ratio_y = self.y_1 - self.y_2
        else:
            self.ratio_x = self.x_2 - self.x_1
            self.ratio_y = self.y_2 - self.y_1

        self.denominator = (self.ratio_x ** 2) + (self.ratio_y ** 2)
        self.denominator = Charles.sqrt(self.denominator)

    def update_rect(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.radius* 2, self.radius * 2)

    def out_of_bounds(self):
        if self.x + self.radius < 0:
            return True
        elif self.x - self.radius > self.display.game.width:
            return True
        elif self.y + self.radius < 0:
            return True
        elif self.y - self.radius > self.display.game.width:
            return True
        return False