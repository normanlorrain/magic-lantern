import pygame
from PIL import Image
from PIL.ExifTags import TAGS
import exifread


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

        with open(filename, "rb") as file_handle:
            # Return Exif tags
            tags = exifread.process_file(file_handle)

        if "EXIF DateTimeOriginal" in tags:
            self.datetime = tags["EXIF DateTimeOriginal"]
        else:
            self.datetime = ""

        # im = Image.open(self.filename)
        # exif = im.getexif()
        # self.datetime = ""
        # for tagid in exif:
        #     # getting the tag name instead of tag id
        #     tagname = TAGS.get(tagid, tagid)
        #     if tagname == tagid:
        #         continue  # tag wasn't found so don't print

        #     # passing the tagid to get its respective value
        #     value = exif.get(tagid)

        #     # printing the final result
        #     print(f"{tagname:25}: {value}")

        #     if tagname == "DateTime":
        #         self.datetime = value
        # pass

    def coordinates(self):
        return (self.x, self.y)

    def getSurface(self):
        return self.surface
