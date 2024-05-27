import os
import itertools
import logging as log

from slideshow.photo import Photo


_photoFileList = []

_photoFileIterator = None


def init(src: str):
    for root, dirs, files in os.walk(src):
        log.info(f"In {root}")
        for f in files:
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                log.warning(f"{f}  Unknown file type")
                continue
            _photoFileList.append(os.path.join(src, f))

    global _photoFileIterator
    _photoFileIterator = itertools.cycle(_photoFileList)
    pass


def getNextPhoto():
    photoFile = next(_photoFileIterator)
    return Photo(photoFile)
