import os
import itertools
import logging as log


_photoList = []

_photoIterator = None


def init(src: str):
    for root, dirs, files in os.walk(src):
        log.info(f"In {root}")
        for f in files:
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                log.warning(f"{f}  Unknown file type")
                continue
            _photoList.append(os.path.join(src, f))

    global _photoIterator
    _photoIterator = itertools.cycle(_photoList)
    pass


def getNextPhoto():
    return next(_photoIterator)
