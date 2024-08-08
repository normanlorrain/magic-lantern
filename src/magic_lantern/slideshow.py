import random

from magic_lantern.photo import Photo
from magic_lantern.album import Album
from magic_lantern.config import Order
from magic_lantern import config
from magic_lantern import log


_photoList: list[Photo] = []
_photoIndex: int = -1
_photoCount: int = 0


def init():
    albumList: list[Album] = []
    albumWeights: list[int] = []
    totalPhotos = 0

    for dictAlbum in config.albums:

        order = dictAlbum[config.ORDER]
        if order not in [e.value for e in Order]:
            raise Exception(f"Bad Config: {order} not in {[e.value for e in Order]}")

        path = config.configRoot / dictAlbum[config.FOLDER]
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
        totalPhotos += album._photoCount

    # Build a list of photos from random albums
    global _photoList
    global _photoCount
    previousAlbum = None
    for album in random.choices(albumList, albumWeights, k=totalPhotos * 100):
        if album._order == Order.ATOMIC:
            if previousAlbum == album:
                log.debug("preventing atomic album from repeating")
                continue
            while photo := album.getNextPhoto():
                _photoList.append(photo)
        else:
            photo = album.getNextPhoto()
            _photoList.append(photo)
        previousAlbum = album
    _photoCount = len(_photoList)


def getNextPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    _photoIndex += 1
    if _photoIndex >= _photoCount:
        _photoIndex = 0
    return _photoList[_photoIndex]


def getPreviousPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    _photoIndex -= 1
    if _photoIndex < 0:
        _photoIndex = 0
    return _photoList[_photoIndex]


def getCurrentPhoto():
    global _photoList
    global _photoIndex
    global _photoCount
    return _photoList[_photoIndex]
