import pygame


class Photo:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.x = 0
        self.y = 0
        self.direction = (0, -1)
        self.velocity = 0
        self.surface = pygame.image.load(self.filename)

    def motion(self):
        pass

    def getSurface(self):
        return self.surface
