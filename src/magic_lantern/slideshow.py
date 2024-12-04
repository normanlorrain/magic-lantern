import random
from pathlib import Path

from magic_lantern.slide import Slide, clearCache
from magic_lantern.album import Album
from magic_lantern.config import Order
from magic_lantern import config
from magic_lantern import log
from magic_lantern.snafu import Snafu

_history: list[Slide] = []
_historyCursor: int = 0


class SlideShowException(Exception):
    pass


def init():
    clearCache()
    _history.clear()

    global _slideGenerator
    _slideGenerator = slideGenerator()


def slideGenerator():
    global _historyCursor
    global _slideCount
    global _history
    global _historyCursor
    _historyCursor = -1
    global _slideCount
    _slideCount = 0
    _previousAlbum = None

    albumList: list[Album] = []
    albumWeights: list[int] = []
    totalSlides = 0

    for dictAlbum in config.albums:
        try:
            order = dictAlbum[config.ORDER]
            if order not in [e.value for e in Order]:
                raise SlideShowException(
                    f"Bad Config: {order} not in {[e.value for e in Order]}"
                )

            path = dictAlbum[config.FOLDER]
            weight = dictAlbum.get(config.WEIGHT, None)
            interval = dictAlbum.get(config.INTERVAL, None)

            album = Album(order, path, weight, interval)
            if album._slideCount > 0:
                albumList.append(album)
                albumWeights.append(album.weight)
                totalSlides += album._slideCount
            else:
                raise SlideShowException(f"Album {path} is empty")
        except SlideShowException as e:
            log.error(e)

    if totalSlides == 0:
        raise Snafu("No images found for slide show.")

    _historyCursor += 1
    if _historyCursor >= _slideCount:
        _historyCursor = 0

    # Get slides from random album
    while True:
        album = random.choices(albumList, albumWeights)[0]
        if album._order == Order.ATOMIC:
            if _previousAlbum == album:
                log.debug("preventing atomic album from repeating")
                continue
            for slide in album:
                yield slide
        else:
            slide = next(album)
            yield slide
        previousAlbum = album


def getNextSlide():
    global _historyCursor
    if _historyCursor < 0:  # current slide is from history
        _historyCursor += 1

    if _historyCursor < 0:
        slide = _history[_historyCursor]
    else:
        slide = next(_slideGenerator)
        _history.append(slide)
        if len(_history) > 10:
            _history.pop(0).unloadImage()

    return slide


def getPreviousSlide():
    global _historyCursor
    if _historyCursor == 0:
        _historyCursor = -2
    else:
        _historyCursor -= 1
    _historyCursor = max(_historyCursor, -len(_history))

    return _history[_historyCursor]
