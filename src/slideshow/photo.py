import pygame
from slideshow import screen


class Photo:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.x = 0
        self.y = 0
        self.direction = (0, -1)
        self.velocity = 0

        # Load the image
        image = pygame.image.load(self.filename)

        # Get the boundary rectangle
        imageRect = pygame.Rect((0, 0), image.get_size())

        # Fit the rectangle to the screen
        imageFit = imageRect.fit(screen.rect())

        self.x = imageFit.x
        self.y = imageFit.y

        # Scale the image to the rectangle
        scaledImage = pygame.transform.scale(image, imageFit.size)

        self.surface = scaledImage.convert()

    def coordinates(self):
        return (self.x, self.y)

    def getSurface(self):
        return self.surface
