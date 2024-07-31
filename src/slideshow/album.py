import os
import pathlib
import random
import enum
import itertools
import logging as log

from slideshow.photo import Photo
from slideshow import config


class Order(enum.StrEnum):
    SEQUENCE = "sequence"
    ATOMIC = "atomic"
    RANDOM = "random"


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

        # Update the photo count
        self._photoCount = len(self._photoFileList)

    def getNextPhoto(self):

        self._photoIndex += 1
        if self._photoIndex >= self._photoCount:
            self._photoIndex = 0
        return Photo(self._photoFileList[self._photoIndex])

    def getPreviousPhoto(self):
        self._photoIndex -= 1
        if self._photoIndex < 0:
            self._photoIndex = self._photoCount - 1
        return Photo(self._photoFileList[self._photoIndex])

    def getCurrentPhoto(self):
        return Photo(self._photoFileList[self._photoIndex])


_albumList: list[Album] = []
_albumIndex: int = 0
_albumCount: int = 0


def init():
    global _albumList
    global _albumCount
    global _albumIndex

    for dictAlbum in config._dictConfig[config.ALBUMS]:

        order = dictAlbum[config.ORDER]
        if order not in Order:
            raise Exception(f"Bad Config: {order} not in {[e.value for e in Order]}")

        path = config._configRoot / dictAlbum[config.FOLDER]
        if not path.exists():
            raise Exception(f"bad Config: invalid path: {path}")

        weight = dictAlbum.get(config.WEIGHT, 0)
        if not isinstance(weight, int):
            raise Exception(f"Bad Config: weight {weight} should be integer")

        album = Album(order, path, weight)
        _albumList.append(album)

    _albumCount = len(_albumList)
    _albumIndex = 0


def getNextPhoto():

    return _albumList[_albumIndex].getNextPhoto()


def getPreviousPhoto():
    return _albumList[_albumIndex].getPreviousPhoto()


def getCurrentPhoto():
    return _albumList[_albumIndex].getCurrentPhoto()
