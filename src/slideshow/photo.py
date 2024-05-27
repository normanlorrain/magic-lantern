import pygame

from slideshow.screen import WIDTH, HEIGHT


class Photo:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.x = 0
        self.y = 0
        self.direction = (0, -1)
        self.velocity = 0
        self.surface = pygame.image.load(self.filename).convert()

    def transform(self):
        return (self.x, self.y)

    def getSurface(self):
        return self.surface
