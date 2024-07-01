import os
import random
import itertools
import logging as log

from slideshow.photo import Photo

_photoFileList = []
_photoIndex = 0
_photoCount = 0


def init(src: os.path, shuffle: bool = False):
    global _photoFileList
    for root, dirs, files in os.walk(os.path.normpath(src)):
        log.info(f"In {root}")
        for f in files:
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                log.warning(f"{f}  Unknown file type")
                continue
            _photoFileList.append(os.path.join(root, f))

    if shuffle:
        random.shuffle(_photoFileList)
    else:
        _photoFileList = sorted(_photoFileList)
    global _photoCount
    _photoCount = len(_photoFileList)


def getNextPhoto():
    global _photoIndex
    _photoIndex += 1
    if _photoIndex >= _photoCount:
        _photoIndex = 0
    return Photo(_photoFileList[_photoIndex])


def getPreviousPhoto():
    global _photoIndex
    _photoIndex -= 1
    if _photoIndex < 0:
        _photoIndex = _photoCount - 1
    return Photo(_photoFileList[_photoIndex])


def getCurrentPhoto():
    return Photo(_photoFileList[_photoIndex])
