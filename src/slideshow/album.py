import os
import random
import itertools
import logging as log

from slideshow.photo import Photo


_photoFileList = []

_photoFileIterator = None


def init(src: os.path):
    for root, dirs, files in os.walk(os.path.normpath(src)):
        log.info(f"In {root}")
        for f in files:
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                log.warning(f"{f}  Unknown file type")
                continue
            _photoFileList.append(os.path.join(root, f))

    random.shuffle(_photoFileList)
    global _photoFileIterator
    _photoFileIterator = itertools.cycle(_photoFileList)
    pass


def getNextPhoto():
    photoFile = next(_photoFileIterator)
    return Photo(photoFile)


# def getPreviousPhoto():
#     photoFile = prev(_photoFileIterator)
#     return Photo(photoFile)
