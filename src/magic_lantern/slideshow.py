import random
from pathlib import Path

from magic_lantern import slide as slidemodule
from magic_lantern.slide import Slide
from magic_lantern.album import Album
from magic_lantern.config import Order
from magic_lantern import config
from magic_lantern import log

_slideList: list[Slide] = []
_slideIndex: int = -1
_slideCount: int = 0


def init():
    slidemodule.init()

    global _slideList
    _slideList.clear()
    global _slideIndex
    _slideIndex = -1
    global _slideCount
    _slideCount = 0

    albumList: list[Album] = []
    albumWeights: list[int] = []
    totalSlides = 0

    for dictAlbum in config.albums:

        order = dictAlbum[config.ORDER]
        if order not in [e.value for e in Order]:
            raise Exception(f"Bad Config: {order} not in {[e.value for e in Order]}")

        path = Path(dictAlbum[config.FOLDER])
        if not path.is_absolute():
            path = config.configRoot / path
        if not path.exists():
            raise Exception(f"bad Config: invalid path: {path}")

        weight = dictAlbum.get(config.WEIGHT, None)
        if weight and not isinstance(weight, int):
            raise Exception(f"Bad Config: weight {weight} should be integer")

        interval = dictAlbum.get(config.INTERVAL, None)
        if interval and not isinstance(interval, int):
            raise Exception(f"Bad Config: interval {interval} should be integer")

        album = Album(order, path, weight, interval)
        albumList.append(album)
        albumWeights.append(album.weight)
        totalSlides += album._slideCount

    if totalSlides == 0:
        raise Exception("No images found for slide show.")

    # Build a list of slides from random albums
    previousAlbum = None
    for album in random.choices(albumList, albumWeights, k=totalSlides * 100):
        if album._order == Order.ATOMIC:
            if previousAlbum == album:
                log.debug("preventing atomic album from repeating")
                continue
            while slide := album.getNextSlide():
                _slideList.append(slide)
        else:
            slide = album.getNextSlide()
            _slideList.append(slide)
        previousAlbum = album
    _slideCount = len(_slideList)


def getNextSlide():
    global _slideList
    global _slideIndex
    global _slideCount
    _slideIndex += 1
    if _slideIndex >= _slideCount:
        _slideIndex = 0
    return _slideList[_slideIndex]


def getPreviousSlide():
    global _slideList
    global _slideIndex
    global _slideCount
    _slideIndex -= 1
    if _slideIndex < 0:
        _slideIndex = 0
    return _slideList[_slideIndex]


def getCurrentSlide():
    global _slideList
    global _slideIndex
    global _slideCount
    return _slideList[_slideIndex]
