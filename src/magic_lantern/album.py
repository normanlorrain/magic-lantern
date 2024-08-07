import os
import pathlib
import random
import logging as log

from magic_lantern.photo import createPhoto, Photo
from magic_lantern import config
from magic_lantern.config import Order
from magic_lantern import pdf


class Album:
    def __init__(self, order: Order, path: pathlib.Path, weight: int = 0):
        """
        Initializes the album with the given source directory.

        Args:
            src (os.path): The path to the source directory.
            shuffle (bool, optional): Whether to shuffle the photos. Defaults to False.
        """
        self._order = order
        self._path = path
        self._weight = weight

        self._photoFileList = []
        self._photoIndex = 0
        self._photoCount = 0
        # Walk through the source directory and its subdirectories
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in config.exclude]
            log.info(f"In {root}")
            for f in files:
                if f.lower().endswith(".pdf"):
                    log.info(f"{f}  PDF file")
                    for pageAsPhoto in pdf.convert(root, f):
                        self._photoFileList.append(pageAsPhoto)
                    continue
                # Filter out files with unknown extensions
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    self._photoFileList.append(os.path.join(root, f))
                    continue

                log.warning(f"{f}  Unknown file type")

        # Shuffle or sort the list of photos
        if self._order == Order.RANDOM:
            random.shuffle(self._photoFileList)
        # else:
        #     self._photoFileList.sort()

        # Update the photo count
        self._photoCount = len(self._photoFileList)

    def getNextPhoto(self):
        if self._photoIndex >= self._photoCount:
            self._photoIndex = 0
            if self._order == Order.ATOMIC:
                return None  # We've reached the end; signal caller
        photo = createPhoto(self._photoFileList[self._photoIndex])
        self._photoIndex += 1
        return photo
