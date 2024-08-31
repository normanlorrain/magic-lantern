import pathlib

import pygame
import exifread

from magic_lantern import screen, log, config

_slideCache: dict = {}


def clearCache():
    _slideCache.clear()


def createSlide(path: str, interval: int):
    if path in _slideCache:
        slide = _slideCache[path]
    else:
        slide = Slide(path, interval)
        _slideCache[path] = slide
    log.info(f"{slide.path.name}")
    return


def getSlide(path: str):
    return _slideCache[path]


class SlideException(Exception):
    def __init__(self, filename):
        self.filename = filename


class Slide:
    def __init__(self, filename, interval) -> None:
        self.filename = filename
        self.path = pathlib.Path(self.filename)
        self.x = 0
        self.y = 0
        self.exif_orientation = None
        self.interval = interval
        self.imageLoaded = False

    def loadImage(self):
        log.debug(f"{self.path.name}")
        if config.exif:
            with open(self.filename, "rb") as file_handle:
                # Return Exif tags
                tags = exifread.process_file(file_handle, details=False)

            if "EXIF DateTimeOriginal" in tags:
                self.datetime = tags["EXIF DateTimeOriginal"]
            if "Image Orientation" in tags.keys():
                self.exif_orientation = tags["Image Orientation"]
        # Load the image
        try:
            image = pygame.image.load(self.filename)
        except:
            raise SlideException(self.filename)

        if 3 in self.exif_orientation.values:
            image = pygame.transform.rotate(image, 180)
        elif 6 in self.exif_orientation.values:
            image = pygame.transform.rotate(image, 270)
        elif 8 in self.exif_orientation.values:
            image = pygame.transform.rotate(image, 90)

        # Get the boundary rectangle
        imageRect = pygame.Rect((0, 0), image.get_size())

        # Fit the rectangle to the screen
        imageFit = imageRect.fit(screen.rect())

        self.x = imageFit.x
        self.y = imageFit.y

        # Scale the image to the rectangle
        scaledImage = pygame.transform.smoothscale(
            image.convert(), imageFit.size
        )  # call convert to upscale any 8-bit images

        self.surface = scaledImage.convert()
        self.datetime = ""

        self.imageLoaded = True

    def coordinates(self):
        if not self.imageLoaded:
            self.loadImage()
        log.debug(f"Coordinates x,y: {self.x},{self.y}")
        return (self.x, self.y)

    def getSurface(self):
        log.info(f"{self.path.name}")
        if not self.imageLoaded:
            self.loadImage()
        return self.surface
