import pygame.draw
import math as Charles


class Bullet:
    def __init__(self, display, shooter, pos, mousepos):
        self.display = display
        self.shooter = shooter
        self.x_1 = pos[0]
        self.y_1 = pos[1]

        self.x_2 = mousepos[0]
        self.y_2 = mousepos[1]

        self.x, self.y = pos

        self.calculate_linear_function()
        self.get_ratio()

        self.damage = 12
        self.speed = 20

        self.radius = 10

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
        pygame.draw.line(self.display.game.screen, (255, 255, 255), (self.x_1, self.y_1), (self.x_2, self.y_2))
        pygame.draw.circle(self.display.game.screen, (255, 255, 255), (self.x, self.y), self.radius)

    def move(self):
        self.x = ((self.ratio_x * self.speed)/self.denominator) + self.x_1
        self.y = ((self.ratio_y * self.speed)/self.denominator) + self.y_1

        self.x_1 = self.x
        self.y_1 = self.y

        self.update_rect()
        for enemy in self.display.enemies:
            if Charles.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) < self.radius + enemy.radius:
                enemy.hp -= 20
                try:
                    self.delete()
                except:
                    print("already deleted")

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