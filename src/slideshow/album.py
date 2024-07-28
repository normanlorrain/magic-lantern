import os
import random
import enum
import itertools
import logging as log

from slideshow.photo import Photo


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


class Album:
    def __init__(self, order: Order, src: os.path, weight: int = 0):
        """
        Initializes the album with the given source directory.

        Args:
            src (os.path): The path to the source directory.
            shuffle (bool, optional): Whether to shuffle the photos. Defaults to False.
        """
        self._order = order
        self._path = src
        self._weight = weight

        self._photoFileList = []
        self._photoIndex = 0
        self._photoCount = 0
        # Walk through the source directory and its subdirectories
        for root, dirs, files in os.walk(os.path.normpath(src)):
            log.info(f"In {root}")
            for f in files:
                # Filter out files with unknown extensions
                if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                    log.warning(f"{f}  Unknown file type")
                    continue
                self._photoFileList.append(os.path.join(root, f))

        # Shuffle or sort the list of photos
        if self._order == Order.RANDOM:
            random.shuffle(self._photoFileList)
        else:
            self._photoFileList = sorted(self._photoFileList)

        # Update the global photo count
        global _photoCount
        _photoCount = len(self._photoFileList)

    def getNextPhoto(self):

        self._photoIndex += 1
        if self._photoIndex >= _photoCount:
            self._photoIndex = 0
        return Photo(self._photoFileList[self._photoIndex])

    def getPreviousPhoto(self):
        self._photoIndex -= 1
        if self._photoIndex < 0:
            self._photoIndex = _photoCount - 1
        return Photo(self._photoFileList[self._photoIndex])

    def getCurrentPhoto(self):
        return Photo(self._photoFileList[self._photoIndex])
