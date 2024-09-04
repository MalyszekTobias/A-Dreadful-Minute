import pygame

class Custom_image:  # A class to easier render images
    def __init__(self, display, path, x, y, w, h):
        self.display = display

        self.x = x  # center x of the image
        self.y = y  # center y of the image
        self.w = w  # width of the image
        self.h = h  # height of the image

        self.path = path  # path to the images

        self.image = pygame.image.load(self.path)  # loading the image
        self.image = pygame.transform.scale(self.image, (self.w, self.h))  # rescaling the image

        self.display.objects.append(self)

    def render(self):  # rendering the image at self.x , self.y
        self.display.screen.blit(self.image, (self.x, self.y))

    def events(self, event):
        pass

    def delete(self):
        self.display.objects.remove(self)
        del self