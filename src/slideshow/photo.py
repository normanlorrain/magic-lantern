import pygame
from PIL import Image
from PIL.ExifTags import TAGS
import exifread


from slideshow import screen

_photoCache: dict = {}


def createPhoto(path: str):
    if path not in _photoCache:
        photo = Photo(path)
        _photoCache[path] = photo
    return _photoCache[path]


class PhotoException(Exception):
    def __init__(self, filename):
        self.filename = filename


class Photo:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.x = 0
        self.y = 0
        self.direction = (0, -1)
        self.velocity = 0

        # Load the image
        try:
            image = pygame.image.load(self.filename)
        except:
            raise PhotoException(self.filename)

        # Get the boundary rectangle
        imageRect = pygame.Rect((0, 0), image.get_size())

        # Fit the rectangle to the screen
        imageFit = imageRect.fit(screen.rect())

        self.x = imageFit.x
        self.y = imageFit.y

        # Scale the image to the rectangle
        scaledImage = pygame.transform.smoothscale(image, imageFit.size)

        self.surface = scaledImage.convert()

        with open(filename, "rb") as file_handle:
            # Return Exif tags
            tags = exifread.process_file(file_handle)

        if "EXIF DateTimeOriginal" in tags:
            self.datetime = tags["EXIF DateTimeOriginal"]
        else:
            self.datetime = ""

    def coordinates(self):
        return (self.x, self.y)

    def getSurface(self):
        return self.surface
