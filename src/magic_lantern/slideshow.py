import random

from magic_lantern.slide import Slide
from magic_lantern.album import Album
from magic_lantern.config import Order
from magic_lantern import config, log
from magic_lantern.snafu import Snafu

_history: list[Slide] = []
_historyCursor: int = 0
_albumList: list[Album] = []
_albumWeights: list[int] = []
_slideGenerator = None
_currentSlide: Slide = None


class SlideShowException(Exception):
    pass


def init():
    totalSlides = 0
    for album in config.albums:
        try:
            if hasattr(album, "order"):
                order = album.order
            else:
                order = config.order
            if order not in [e.value for e in Order]:
                raise SlideShowException(
                    f"Bad Config: {order} not in {[e.value for e in Order]}"
                )

            path = album.folder
            weight = album.weight
            interval = album.interval

            album = Album(order, path, weight, interval)
            if album._slideCount > 0:
                _albumList.append(album)
                _albumWeights.append(album.weight)
                totalSlides += album._slideCount
            else:
                raise SlideShowException(f"Album {path} is empty")
        except SlideShowException as e:
            log.error(e)

    if totalSlides == 0:
        raise Snafu("No images found for slide show.")

    global _slideGenerator
    _slideGenerator = slideGenerator()


def slideGenerator():
    # Get slides from random album
    while True:
        album = random.choices(_albumList, _albumWeights)[0]
        if album._order == Order.ATOMIC:
            yield from album
        else:
            try:
                slide = next(album)
                yield slide
            except StopIteration:
                pass


def getNextSlide():
    global _historyCursor
    if _historyCursor < 0:  # current slide is from history
        _historyCursor += 1

    if _historyCursor < 0:
        slide = _history[_historyCursor]
    else:
        slide = next(_slideGenerator)
        _history.append(slide)

        # Important.  The slide will still exists (it's in the album)
        # but we unload the image otherwise large slideshows eat
        # memory.
        if len(_history) > 10:
            _history.pop(0).unloadImage()
    global _currentSlide
    _currentSlide = slide
    return slide


def getPreviousSlide():
    global _historyCursor
    if _historyCursor == 0:
        _historyCursor = -2
    else:
        _historyCursor -= 1
    _historyCursor = max(_historyCursor, -len(_history))
    slide = _history[_historyCursor]

    global _currentSlide
    _currentSlide = slide
    return _currentSlide


def getCurrentSlide():
    return _currentSlide
