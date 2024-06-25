import pygame
from slideshow import screen


class Photo:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.x = 0
        self.y = 0
        self.direction = (0, -1)
        self.velocity = 0
        image = pygame.image.load(self.filename)

        rect = pygame.Rect(0, 0, image.get_width(), image.get_height())
        self.rect = rect.fit(screen.rect())

        image = pygame.transform.scale(image, self.rect.size)
        self.surface = image.convert()

    def transform(self):
        return (self.x, self.y)

    def getSurface(self):
        return self.surface
