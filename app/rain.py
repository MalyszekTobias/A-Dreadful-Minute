import random, pygame
class Rain:
    def __init__(self, display, amount):
        self.display = display
        self.amount = amount
        self.speed = 10

        self.drops = [Drop(self) for x in range(self.amount)]

    def render(self):
        for drop in self.drops:
            drop.render()

    def events(self, event):
        pass

    def move(self):
        for drop in self.drops:
            drop.move()




class Drop:
    def __init__(self, cloud):
        self.x = random.randint(0, cloud.display.game.width)
        self.y = random.randint(0, cloud.display.game.height)
        self.cloud = cloud
        self.w = 3
        self.h = 30

        self.color = (random.randint(10, 50), random.randint(87, 127), random.randint(150, 190))

    def render(self):
        pygame.draw.rect(self.cloud.display.game.screen, self.color, (self.x, self.y, self.w, self.h))

    def move(self):
        self.y += self.cloud.speed
        if self.y >= self.cloud.display.game.height:
            self.y = 0 - self.h
